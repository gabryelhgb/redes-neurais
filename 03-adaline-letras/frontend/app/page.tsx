"use client";

import { useEffect, useRef, useState, type PointerEvent } from "react";

type Amostra = {
  letra: string;
  fonte: number;
  grade: number[][];
};

type Catalogo = {
  letras: string[];
  fontes: number[];
  amostras: Amostra[];
};

type Treinamento = {
  ciclos: number;
  eqm_final: number;
  convergiu: boolean;
  historico_eqm: number[];
};

type ResultadoTeste = {
  letras_reconhecidas: string[];
};

type Pincel = 1 | 0;

const API = "http://127.0.0.1:8000";

function novaGrade(): number[][] {
  return Array.from({ length: 9 }, () => Array(7).fill(-1));
}

async function exigirSucesso(resposta: Response) {
  if (resposta.ok) return;

  const dados = (await resposta.json().catch(() => null)) as
    | { detail?: string }
    | null;

  throw new Error(dados?.detail ?? `Erro HTTP ${resposta.status}`);
}

function mensagemErro(falha: unknown): string {
  return falha instanceof Error ? falha.message : "Ocorreu um erro inesperado.";
}

function GradeReferencia({ grade }: { grade: number[][] }) {
  return (
    <div className="grid w-max grid-cols-7 gap-1">
      {grade.flatMap((linha, indiceLinha) =>
        linha.map((pixel, indiceColuna) => (
          <div
            key={`${indiceLinha}-${indiceColuna}`}
            className={`flex h-8 w-8 items-center justify-center rounded text-sm font-bold ${
              pixel === 1
                ? "bg-emerald-700 text-white"
                : "bg-slate-100 text-slate-400"
            }`}
          >
            {pixel === 1 ? "#" : "·"}
          </div>
        )),
      )}
    </div>
  );
}

export default function Home() {
  const [catalogo, setCatalogo] = useState<Catalogo | null>(null);
  const [fonte, setFonte] = useState(1);
  const [letra, setLetra] = useState("A");
  const [gradeTeste, setGradeTeste] = useState<number[][]>(novaGrade);
  const [pincel, setPincel] = useState<Pincel>(1);
  const [treinamento, setTreinamento] = useState<Treinamento | null>(null);
  const [resultado, setResultado] = useState<ResultadoTeste | null>(null);
  const [erro, setErro] = useState("");
  const [carregando, setCarregando] = useState(true);
  const [treinando, setTreinando] = useState(false);
  const [testando, setTestando] = useState(false);

  const valorArrasto = useRef<number | null>(null);

  useEffect(() => {
    fetch(`${API}/amostras`)
      .then(async (resposta) => {
        await exigirSucesso(resposta);
        return (await resposta.json()) as Catalogo;
      })
      .then(setCatalogo)
      .catch((falha) => setErro(mensagemErro(falha)))
      .finally(() => setCarregando(false));
  }, []);

  const amostraAtual = catalogo?.amostras.find(
    (amostra) => amostra.fonte === fonte && amostra.letra === letra,
  );

  const historico = treinamento?.historico_eqm ?? [];
  const maiorEqm = Math.max(1, ...historico);
  const pontosGrafico = historico
    .map((valor, indice) => {
      const x = 20 + (indice / Math.max(1, historico.length - 1)) * 560;
      const y = 170 - (valor / maiorEqm) * 145;
      return `${x},${y}`;
    })
    .join(" ");

  function pintar(linha: number, coluna: number, valor: number) {
    setGradeTeste((gradeAnterior) => {
      if (gradeAnterior[linha][coluna] === valor) return gradeAnterior;

      return gradeAnterior.map((pixels, indiceLinha) =>
        indiceLinha === linha
          ? pixels.map((pixel, indiceColuna) =>
              indiceColuna === coluna ? valor : pixel,
            )
          : pixels,
      );
    });

    setResultado(null);
  }

  function iniciarPintura(
    evento: PointerEvent<HTMLButtonElement>,
    linha: number,
    coluna: number,
  ) {
    if (evento.pointerType === "mouse" && evento.button !== 0) return;

    evento.preventDefault();

    const novoValor = gradeTeste[linha][coluna] === pincel ? -1 : pincel;
    valorArrasto.current = novoValor;

    evento.currentTarget.setPointerCapture(evento.pointerId);
    pintar(linha, coluna, novoValor);
  }

  function moverPincel(evento: PointerEvent<HTMLButtonElement>) {
    if (valorArrasto.current === null) return;

    const celula = document
      .elementFromPoint(evento.clientX, evento.clientY)
      ?.closest("[data-celula]");

    if (!celula) return;

    const linha = Number(celula.getAttribute("data-linha"));
    const coluna = Number(celula.getAttribute("data-coluna"));

    pintar(linha, coluna, valorArrasto.current);
  }

  function copiarAmostra() {
    if (!amostraAtual) return;

    setGradeTeste(amostraAtual.grade.map((linha) => [...linha]));
    setResultado(null);
  }

  async function treinar() {
    setErro("");
    setResultado(null);
    setTreinamento(null);
    setTreinando(true);

    try {
      const resposta = await fetch(`${API}/treinar`, { method: "POST" });
      await exigirSucesso(resposta);

      const dados = (await resposta.json()) as Treinamento;
      setTreinamento(dados);
    } catch (falha) {
      setErro(mensagemErro(falha));
    } finally {
      setTreinando(false);
    }
  }

  async function testar() {
    setErro("");
    setResultado(null);
    setTestando(true);

    try {
      const resposta = await fetch(`${API}/testar`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ grade: gradeTeste }),
      });

      await exigirSucesso(resposta);

      const dados = (await resposta.json()) as ResultadoTeste;
      setResultado(dados);
    } catch (falha) {
      setErro(mensagemErro(falha));
    } finally {
      setTestando(false);
    }
  }

  return (
    <main className="min-h-screen px-3 py-8 sm:px-6">
      <div className="mx-auto max-w-7xl">
        <header className="mb-8">
          <p className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-700">
            Redes neurais • avaliação
          </p>
          <h1 className="mt-2 font-serif text-4xl font-bold tracking-tight">
            Reconhecimento de letras com Adaline
          </h1>
          <p className="mt-2 text-slate-600">
            Treine com três fontes e teste uma letra desenhada em 9 × 7 pixels.
          </p>
        </header>

        {erro && (
          <p role="alert" className="mb-6 rounded-lg bg-red-50 p-4 text-red-800">
            {erro}
          </p>
        )}

        <div className="grid gap-6 lg:grid-cols-2">
          <section className="rounded-2xl bg-white p-4 shadow-sm sm:p-6">
            <h2 className="text-xl font-bold">Base de treinamento</h2>
            <p className="mt-1 text-sm text-slate-600">
              Escolha uma das 21 amostras para visualizar.
            </p>

            <div className="mt-5 flex flex-wrap gap-4">
              <label className="text-sm font-semibold">
                Fonte
                <select
                  value={fonte}
                  onChange={(evento) => setFonte(Number(evento.target.value))}
                  className="mt-1 block rounded-lg border border-slate-300 bg-slate-50 px-3 py-2"
                >
                  {(catalogo?.fontes ?? [1, 2, 3]).map((opcao) => (
                    <option key={opcao} value={opcao}>
                      {opcao}
                    </option>
                  ))}
                </select>
              </label>

              <label className="text-sm font-semibold">
                Letra
                <select
                  value={letra}
                  onChange={(evento) => setLetra(evento.target.value)}
                  className="mt-1 block rounded-lg border border-slate-300 bg-slate-50 px-3 py-2"
                >
                  {(catalogo?.letras ?? ["A", "B", "C", "D", "E", "J", "K"]).map(
                    (opcao) => (
                      <option key={opcao} value={opcao}>
                        {opcao}
                      </option>
                    ),
                  )}
                </select>
              </label>
            </div>

            <div className="mt-6 overflow-x-auto">
              {amostraAtual ? (
                <GradeReferencia grade={amostraAtual.grade} />
              ) : (
                <p className="text-sm text-slate-500">
                  {carregando ? "Carregando amostras..." : "Amostra indisponível."}
                </p>
              )}
            </div>

            <div className="mt-6 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={treinar}
                disabled={treinando}
                className="min-h-11 rounded-lg bg-emerald-700 px-5 font-semibold text-white hover:bg-emerald-800 disabled:opacity-50"
              >
                {treinando ? "Treinando..." : "Treinar rede"}
              </button>

              <button
                type="button"
                onClick={copiarAmostra}
                disabled={!amostraAtual}
                className="min-h-11 rounded-lg border border-slate-300 px-4 font-semibold hover:bg-slate-50 disabled:opacity-50"
              >
                Copiar para teste
              </button>
            </div>

            <div className="mt-8 rounded-xl bg-slate-50 p-4">
              <h3 className="font-bold">Erro quadrático médio</h3>

              {treinamento ? (
                <>
                  <p className="mt-1 text-sm text-slate-600">
                    {treinamento.ciclos} ciclos • EQM final{" "}
                    {treinamento.eqm_final.toExponential(4)} •{" "}
                    {treinamento.convergiu
                      ? "critério atingido"
                      : "limite de ciclos atingido"}
                  </p>

                  <svg
                    viewBox="0 0 600 200"
                    role="img"
                    aria-label="Gráfico do erro quadrático médio por ciclo"
                    className="mt-4 w-full"
                  >
                    <line
                      x1="20"
                      y1="170"
                      x2="580"
                      y2="170"
                      stroke="#94a3b8"
                    />
                    <line
                      x1="20"
                      y1="20"
                      x2="20"
                      y2="170"
                      stroke="#94a3b8"
                    />
                    <polyline
                      points={pontosGrafico}
                      fill="none"
                      stroke="#047857"
                      strokeWidth="3"
                    />
                    <text x="20" y="190" fontSize="12" fill="#475569">
                      1
                    </text>
                    <text x="540" y="190" fontSize="12" fill="#475569">
                      {treinamento.ciclos} ciclos
                    </text>
                  </svg>
                </>
              ) : (
                <p className="mt-2 text-sm text-slate-500">
                  Treine a rede para visualizar a curva do EQM.
                </p>
              )}
            </div>
          </section>

          <section className="rounded-2xl bg-white p-4 shadow-sm sm:p-6">
            <h2 className="text-xl font-bold">Teste da rede neural</h2>
            <p className="mt-1 text-sm text-slate-600">
              Clique ou arraste para desenhar. Clicar novamente em um pixel
              selecionado apaga esse pixel.
            </p>

            <div className="mt-5 flex flex-wrap gap-3">
              <button
                type="button"
                onClick={() => setPincel(1)}
                aria-pressed={pincel === 1}
                className={`min-h-11 rounded-lg px-4 font-semibold ${
                  pincel === 1
                    ? "bg-emerald-700 text-white"
                    : "bg-slate-100 text-slate-700"
                }`}
              >
                Desenhar
              </button>

              <button
                type="button"
                onClick={() => setPincel(0)}
                aria-pressed={pincel === 0}
                className={`min-h-11 rounded-lg px-4 font-semibold ${
                  pincel === 0
                    ? "bg-amber-300 text-amber-950"
                    : "bg-slate-100 text-slate-700"
                }`}
              >
                Marcar ruído
              </button>

              <button
                type="button"
                onClick={() => {
                  setGradeTeste(novaGrade());
                  setResultado(null);
                }}
                className="min-h-11 rounded-lg border border-slate-300 px-4 font-semibold hover:bg-slate-50"
              >
                Limpar
              </button>
            </div>

            <div className="mt-6 overflow-x-auto">
              <div className="grid w-max grid-cols-7 gap-1">
                {gradeTeste.flatMap((linha, indiceLinha) =>
                  linha.map((pixel, indiceColuna) => (
                    <button
                      key={`${indiceLinha}-${indiceColuna}`}
                      type="button"
                      data-celula
                      data-linha={indiceLinha}
                      data-coluna={indiceColuna}
                      aria-label={`Linha ${indiceLinha + 1}, coluna ${
                        indiceColuna + 1
                      }: ${
                        pixel === 1
                          ? "pintado"
                          : pixel === 0
                            ? "ruído"
                            : "vazio"
                      }`}
                      onPointerDown={(evento) =>
                        iniciarPintura(evento, indiceLinha, indiceColuna)
                      }
                      onPointerMove={moverPincel}
                      onPointerUp={() => {
                        valorArrasto.current = null;
                      }}
                      onPointerCancel={() => {
                        valorArrasto.current = null;
                      }}
                      onKeyDown={(evento) => {
                        if (evento.key === "Enter" || evento.key === " ") {
                          evento.preventDefault();
                          pintar(
                            indiceLinha,
                            indiceColuna,
                            pixel === pincel ? -1 : pincel,
                          );
                        }
                      }}
                      className={`h-10 w-10 touch-none rounded font-bold focus-visible:outline-2 focus-visible:outline-emerald-700 sm:h-11 sm:w-11 ${
                        pixel === 1
                          ? "bg-emerald-700 text-white"
                          : pixel === 0
                            ? "bg-amber-200 text-amber-950"
                            : "bg-slate-100 text-slate-400 hover:bg-slate-200"
                      }`}
                    >
                      {pixel === 1 ? "#" : pixel === 0 ? "0" : "·"}
                    </button>
                  )),
                )}
              </div>
            </div>

            <p className="mt-4 text-sm text-slate-600">
              Verde = pixel ativo (1); claro = inativo (-1); amarelo = ruído (0).
            </p>

            <button
              type="button"
              onClick={testar}
              disabled={!treinamento || testando}
              className="mt-6 min-h-11 rounded-lg bg-emerald-700 px-5 font-semibold text-white hover:bg-emerald-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {testando ? "Testando..." : "Testar letra"}
            </button>

            <div className="mt-6 rounded-xl bg-slate-50 p-5">
              <p className="text-sm font-semibold uppercase tracking-wide text-slate-600">
                Resposta da rede neural
              </p>
              <p className="mt-2 text-3xl font-bold text-emerald-800">
                {resultado
                  ? resultado.letras_reconhecidas.length > 0
                    ? resultado.letras_reconhecidas.join(", ")
                    : "Nenhuma letra reconhecida"
                  : "—"}
              </p>
            </div>
          </section>
        </div>
      </div>
    </main>
  );
}