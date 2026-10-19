"use client";

import { useEffect, useState, type FormEvent } from "react";

type Configuracao = {
  taxa: number;
  momento: number;
  ciclos: number;
  limite_pesos: number;
  semente: number;
};

type Amostra = { x: number; desejado: number };
type Comparacao = Amostra & { previsto: number };

type Treinamento = {
  parametros: Configuracao;
  ciclos: number;
  eqm_inicial: number;
  eqm_final: number;
  historico_eqm: number[];
  comparacao: Comparacao[];
  pesos: { v: number[]; bias_v: number[]; w: number[]; bias_w: number };
  tempo_segundos: number;
};

type Curva = {
  nome: string;
  cor: string;
  pontos: { x: number; y: number }[];
  tracejada?: boolean;
};

const API = "http://127.0.0.1:8000";

const campos: {
  chave: keyof Configuracao;
  nome: string;
  passo: string;
  minimo: string;
  maximo?: string;
}[] = [
  { chave: "taxa", nome: "Taxa de aprendizagem", passo: "any", minimo: "0.000001" },
  { chave: "momento", nome: "Momento", passo: "any", minimo: "0", maximo: "0.999999" },
  { chave: "ciclos", nome: "Quantidade de ciclos", passo: "1", minimo: "1" },
  { chave: "limite_pesos", nome: "Limite dos pesos iniciais (±)", passo: "any", minimo: "0.000001" },
  { chave: "semente", nome: "Semente aleatória", passo: "1", minimo: "0" },
];

async function lerResposta(resposta: Response): Promise<unknown> {
  const dados: unknown = await resposta.json();

  if (!resposta.ok) {
    const detalhe = typeof dados === "object" && dados !== null && "detail" in dados
      ? dados.detail
      : null;

    throw new Error(typeof detalhe === "string"
      ? detalhe
      : "Confira os parâmetros: use valores numéricos válidos.");
  }

  return dados;
}

function mensagemErro(falha: unknown) {
  if (falha instanceof TypeError) {
    return "Não foi possível acessar a API. Confira se o backend está rodando na porta 8000.";
  }
  return falha instanceof Error ? falha.message : "Ocorreu um erro inesperado.";
}

function Grafico({ titulo, curvas, eixoX, limitesY }: {
  titulo: string;
  curvas: Curva[];
  eixoX: string;
  limitesY?: [number, number];
}) {
  const pontos = curvas.flatMap((curva) => curva.pontos);
  const minimoX = pontos.reduce((menor, ponto) => Math.min(menor, ponto.x), Infinity);
  const maximoX = pontos.reduce((maior, ponto) => Math.max(maior, ponto.x), -Infinity);
  const minimoY = limitesY?.[0] ?? 0;
  const maximoY = limitesY?.[1] ?? pontos.reduce((maior, ponto) => Math.max(maior, ponto.y), 1e-12);

  const escalaX = (x: number) => 60 + ((x - minimoX) / Math.max(maximoX - minimoX, 1e-12)) * 620;
  const escalaY = (y: number) => 220 - ((y - minimoY) / (maximoY - minimoY)) * 200;
  const marcas = [0, 0.25, 0.5, 0.75, 1];

  return (
    <section className="painel">
      <h2 className="text-xl font-semibold">{titulo}</h2>
      {pontos.length === 0 ? (
        <p className="muted py-16">Os dados aparecerão aqui após o treinamento.</p>
      ) : (
        <>
          <div className="mt-3 flex flex-wrap gap-4 text-sm">
            {curvas.map((curva) => (
              <span key={curva.nome} className="flex items-center gap-2">
                <span aria-hidden="true" style={{ background: curva.cor }} className="h-1 w-5" />
                {curva.nome}
              </span>
            ))}
          </div>
          <svg viewBox="0 0 720 280" role="img" aria-label={titulo} className="mt-3 w-full">
            {marcas.map((fracao) => {
              const y = 220 - fracao * 200;
              const valor = minimoY + fracao * (maximoY - minimoY);
              return (
                <g key={fracao}>
                  <line x1="60" y1={y} x2="680" y2={y} stroke="var(--linha)" strokeDasharray="4 4" />
                  <text x="52" y={y + 4} textAnchor="end" fontSize="11" fill="var(--muted)">
                    {maximoY < 0.01 ? valor.toExponential(1) : valor.toFixed(2)}
                  </text>
                </g>
              );
            })}
            {marcas.map((fracao) => {
              const x = 60 + fracao * 620;
              const valor = minimoX + fracao * (maximoX - minimoX);
              return (
                <g key={fracao}>
                  <line x1={x} y1="20" x2={x} y2="220" stroke="var(--linha)" />
                  <text x={x} y="243" textAnchor="middle" fontSize="11" fill="var(--muted)">
                    {eixoX === "Ciclos" ? Math.round(valor) : valor.toFixed(2)}
                  </text>
                </g>
              );
            })}
            {curvas.map((curva) => (
              <polyline
                key={curva.nome}
                points={curva.pontos.map((ponto) => `${escalaX(ponto.x).toFixed(2)},${escalaY(ponto.y).toFixed(2)}`).join(" ")}
                fill="none"
                stroke={curva.cor}
                strokeWidth="2.5"
                strokeDasharray={curva.tracejada ? "6 4" : undefined}
                strokeLinejoin="round"
              />
            ))}
            <text x="370" y="272" textAnchor="middle" fontSize="12" fill="var(--muted)">{eixoX}</text>
          </svg>
        </>
      )}
    </section>
  );
}

export default function Home() {
  const [valores, setValores] = useState<Record<keyof Configuracao, string>>({
    taxa: "0.5", momento: "0.05", ciclos: "35000",
    limite_pesos: "0.3333333333333333", semente: "42",
  });
  const [amostras, setAmostras] = useState<Amostra[]>([]);
  const [resultado, setResultado] = useState<Treinamento | null>(null);
  const [treinando, setTreinando] = useState(false);
  const [erro, setErro] = useState("");

  useEffect(() => {
    const controlador = new AbortController();
    fetch(`${API}/amostras`, { signal: controlador.signal })
      .then(lerResposta)
      .then((dados) => setAmostras((dados as { amostras: Amostra[] }).amostras))
      .catch((falha: unknown) => {
        if (!controlador.signal.aborted) setErro(mensagemErro(falha));
      });
    return () => controlador.abort();
  }, []);

  async function treinar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setErro("");
    setResultado(null);
    setTreinando(true);

    const parametros: Configuracao = {
      taxa: Number(valores.taxa), momento: Number(valores.momento),
      ciclos: Number(valores.ciclos), limite_pesos: Number(valores.limite_pesos),
      semente: Number(valores.semente),
    };

    try {
      const resposta = await fetch(`${API}/treinar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(parametros),
      });
      const dados = await lerResposta(resposta) as Treinamento;
      setResultado(dados);
    } catch (falha) {
      setErro(mensagemErro(falha));
    } finally {
      setTreinando(false);
    }
  }

  const referencias = resultado?.comparacao ?? amostras;
  const curvasFuncao: Curva[] = [{
    nome: "Função real", cor: "var(--alvo)", tracejada: true,
    pontos: referencias.map((ponto) => ({ x: ponto.x, y: ponto.desejado })),
  }];
  if (resultado) curvasFuncao.push({
    nome: "Previsão da rede", cor: "var(--rede)",
    pontos: resultado.comparacao.map((ponto) => ({ x: ponto.x, y: ponto.previsto })),
  });

  return (
    <main className="mx-auto max-w-6xl space-y-6 p-4 sm:p-8">
      <header>
        <p className="muted text-sm">Exercício 04 · Rede 1 → 10 → 1</p>
        <h1 className="mt-2 text-3xl font-bold tracking-tight">Aproximação de função</h1>
        <p className="muted mt-2">Backpropagation para aprender f(x) = sen(x) × sen(2x).</p>
      </header>

      <section className="painel">
        <h2 className="text-xl font-semibold">Parâmetros do treinamento</h2>
        <form onSubmit={treinar} className="mt-4">
          <fieldset disabled={treinando} className="grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
            <legend className="sr-only">Configure os cinco parâmetros</legend>
            {campos.map((campo) => (
              <label key={campo.chave} className="text-sm font-medium">
                {campo.nome}
                <input
                  type="number" required step={campo.passo} min={campo.minimo} max={campo.maximo}
                  value={valores[campo.chave]}
                  onChange={(evento) => setValores((anteriores) => ({ ...anteriores, [campo.chave]: evento.target.value }))}
                />
              </label>
            ))}
            <button type="submit" className="sm:col-span-2 lg:col-span-5 justify-self-start">
              {treinando ? "Treinando…" : "Treinar rede"}
            </button>
          </fieldset>
        </form>
        <p className="muted mt-3 text-sm">Mantenha a mesma semente para comparar parâmetros usando os mesmos pesos iniciais.</p>
      </section>

      {erro && <p role="alert" className="erro">{erro}</p>}
      <div role="status" aria-live="polite">
        {treinando && <p className="muted">Treinamento em andamento. Aguarde; o resultado aparecerá ao terminar.</p>}
        {resultado && (
          <div className="painel grid gap-4 tabular-nums sm:grid-cols-3">
            <div><p className="muted text-sm">EQM final</p><p className="text-2xl font-semibold">{resultado.eqm_final.toExponential(5)}</p></div>
            <div><p className="muted text-sm">Ciclos executados</p><p className="text-2xl font-semibold">{resultado.ciclos.toLocaleString("pt-BR")}</p></div>
            <div><p className="muted text-sm">Tempo de execução</p><p className="text-2xl font-semibold">{resultado.tempo_segundos.toFixed(2)} s</p></div>
          </div>
        )}
      </div>

      <Grafico titulo="Função real × previsão" curvas={curvasFuncao} eixoX="x (radianos)" limitesY={[-1, 1]} />
      <Grafico titulo="Erro quadrático médio por ciclo" eixoX="Ciclos" curvas={resultado ? [{
        nome: "EQM", cor: "var(--acao)",
        pontos: resultado.historico_eqm.map((y, x) => ({ x, y })),
      }] : []} />

      {resultado && (
        <section className="painel overflow-x-auto">
          <h2 className="text-xl font-semibold">Pesos após o treinamento</h2>
          <p className="muted mt-2 text-sm">Bias da saída: {resultado.pesos.bias_w.toFixed(6)}. Existe um único bias na saída.</p>
          <table className="dados mt-4 w-full text-sm tabular-nums">
            <caption className="sr-only">Pesos dos dez neurônios ocultos</caption>
            <thead><tr><th>Neurônio</th><th>Peso V</th><th>Bias V</th><th>Peso W</th></tr></thead>
            <tbody>{resultado.pesos.v.map((v, indice) => (
              <tr key={indice}>
                <td>{indice + 1}</td><td>{v.toFixed(6)}</td>
                <td>{resultado.pesos.bias_v[indice].toFixed(6)}</td>
                <td>{resultado.pesos.w[indice].toFixed(6)}</td>
              </tr>
            ))}</tbody>
          </table>
        </section>
      )}
    </main>
  );
}