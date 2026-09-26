"use client";

import { useState, type FormEvent } from "react";

type ResultadoTreinamento = {
  mensagem: string;
  ciclos: number;
  pesos: number[];
};

type ResultadoTeste = {
  resposta: number;
  diagnostico: string;
};

type ErroApi = {
  erro: string;
};

export default function Home() {
  const [treinamento, setTreinamento] =
    useState<ResultadoTreinamento | null>(null);
  const [resultado, setResultado] = useState<ResultadoTeste | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [treinando, setTreinando] = useState(false);
  const [testando, setTestando] = useState(false);

  async function treinar() {
    setErro(null);
    setResultado(null);
    setTreinamento(null);
    setTreinando(true);

    try {
      const respostaApi = await fetch("http://localhost:8000/treinar", {
        method: "POST",
      });

      if (!respostaApi.ok) {
        throw new Error(`Erro HTTP ${respostaApi.status}`);
      }

      const dados: ResultadoTreinamento = await respostaApi.json();
      setTreinamento(dados);
    } catch {
      setErro("Não foi possível treinar. Confira se a API está rodando.");
    } finally {
      setTreinando(false);
    }
  }

  async function testar(evento: FormEvent<HTMLFormElement>) {
    evento.preventDefault();
    setErro(null);
    setResultado(null);
    setTestando(true);

    const formulario = new FormData(evento.currentTarget);

    const dadosPaciente = {
      febre: formulario.get("febre") === "1" ? 1 : -1,
      nausea: formulario.get("nausea") === "1" ? 1 : -1,
      manchas: Number(formulario.get("manchas")),
      dor: formulario.get("dor") === "1" ? 1 : -1,
    };

    try {
      const respostaApi = await fetch("http://localhost:8000/testar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dadosPaciente),
      });

      if (!respostaApi.ok) {
        throw new Error(`Erro HTTP ${respostaApi.status}`);
      }

      const dados: ResultadoTeste | ErroApi = await respostaApi.json();

      if ("erro" in dados) {
        throw new Error(dados.erro);
      }

      setResultado(dados);
    } catch (erroRecebido) {
      setErro(
        erroRecebido instanceof Error
          ? erroRecebido.message
          : "Não foi possível testar o paciente."
      );
    } finally {
      setTestando(false);
    }
  }

  return (
    <main className="min-h-screen bg-stone-100 px-6 py-12 text-stone-900">
      <section className="mx-auto max-w-2xl">
        <p className="text-sm font-semibold uppercase tracking-widest text-emerald-800">
          Projeto de redes neurais
        </p>

        <h1 className="mt-3 text-3xl font-bold">
          Perceptron de diagnóstico
        </h1>

        <button
          type="button"
          onClick={treinar}
          disabled={treinando}
          className="mt-6 min-h-11 rounded-lg bg-emerald-800 px-5 font-semibold text-white disabled:opacity-50"
        >
          {treinando ? "Treinando..." : "Treinar"}
        </button>

        {treinamento && (
          <section className="mt-5 rounded-2xl bg-white p-5 shadow-sm">
            <h2 className="text-xl font-bold">Treinamento concluído</h2>
            <p className="mt-2">Ciclos: {treinamento.ciclos}</p>
            <p>Pesos finais: [{treinamento.pesos.join(", ")}]</p>
          </section>
        )}

        <form
          onSubmit={testar}
          className="mt-8 space-y-5 rounded-2xl bg-white p-6 shadow-sm"
        >
          <p className="text-stone-600">
            Marque os sintomas presentes e escolha o tamanho das manchas.
          </p>

          {[
            ["Febre", "febre"],
            ["Náusea", "nausea"],
            ["Dor", "dor"],
          ].map(([rotulo, nome]) => (
            <label key={nome} className="flex min-h-11 items-center gap-3">
              <input
                type="checkbox"
                name={nome}
                value="1"
                className="size-5 accent-emerald-800"
              />
              {rotulo}
            </label>
          ))}

          <fieldset>
            <legend className="font-semibold">Tamanho das manchas</legend>

            <label className="mt-3 flex min-h-11 items-center gap-3">
              <input
                type="radio"
                name="manchas"
                value="1"
                required
                className="size-5 accent-emerald-800"
              />
              Pequenas
            </label>

            <label className="flex min-h-11 items-center gap-3">
              <input
                type="radio"
                name="manchas"
                value="-1"
                className="size-5 accent-emerald-800"
              />
              Grandes
            </label>
          </fieldset>

          <button
            type="submit"
            disabled={!treinamento || testando}
            className="min-h-11 rounded-lg bg-stone-800 px-5 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
          >
            {testando ? "Testando..." : "Testar paciente"}
          </button>

          {resultado && (
            <section aria-live="polite" className="rounded-xl bg-stone-50 p-5">
              <h2 className="text-xl font-bold">
                Diagnóstico: {resultado.diagnostico}
              </h2>
              <p className="mt-2">Resposta da rede: {resultado.resposta}</p>
            </section>
          )}

          {erro && (
            <p role="alert" className="text-red-700">
              {erro}
            </p>
          )}
        </form>
      </section>
    </main>
  );
}