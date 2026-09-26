"use client";

import { useState } from "react";

const caracteristicas = [
  { nome: "Raciocínio lógico", id: "raciocinio" },
  { nome: "Persistente", id: "persistente" },
  { nome: "Estudioso", id: "estudioso" },
  { nome: "Decidido", id: "decidido" },
];

type ResultadoClassificacao = {
  resposta: number;
  perfil: string;
};

export default function Home() {

  const [resultado, setResultado] =
    useState<ResultadoClassificacao | null>(null);
  const [erro, setErro] = useState<string | null>(null);
  const [carregando, setCarregando] = useState(false);

  async function classificar(evento: React.FormEvent<HTMLFormElement>) {
    evento.preventDefault();

    const formulario = new FormData(evento.currentTarget);

    const novasRespostas = [
      formulario.get("raciocinio"),
      formulario.get("persistente"),
      formulario.get("estudioso"),
      formulario.get("decidido"),
    ].map(Number);

    const dadosPerfil = {
      raciocinio_logico: novasRespostas[0],
      persistente: novasRespostas[1],
      estudioso: novasRespostas[2],
      decidido: novasRespostas[3],
    };

    setErro(null);
    setResultado(null);
    setCarregando(true);

    try {
      const respostaApi = await fetch("http://localhost:8000/classificar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(dadosPerfil),
      });

      if (!respostaApi.ok) {
        throw new Error(`Erro HTTP ${respostaApi.status}`);
      }

      const dadosRetornados: ResultadoClassificacao = await respostaApi.json();
      setResultado(dadosRetornados);
    } catch {
      setErro(
        "Não foi possível classificar. Confira se a API está rodando e tente novamente."
      );
    } finally {
      setCarregando(false);
    }
  }

  return (
    <main className="min-h-screen bg-stone-100 px-6 py-12 text-stone-900">
      <section className="mx-auto max-w-2xl">
        <p className="text-sm font-semibold uppercase tracking-widest text-emerald-800">
          Projeto de redes neurais
        </p>

        <h1 className="mt-3 text-3xl font-bold">
          Perfil acadêmico
        </h1>

        <p className="mt-3 leading-7 text-stone-600">
          Responda às quatro perguntas para descobrir com qual perfil acadêmico
          a rede neural identifica maior compatibilidade.
        </p>

        <form className="mt-8 space-y-5 rounded-2xl bg-white p-6 shadow-sm" onSubmit={classificar}>
          {caracteristicas.map((caracteristica) => (
            <fieldset
              key={caracteristica.id}
              className="border-b border-stone-200 pb-5 last:border-b-0"
            >
              <legend className="font-semibold">
                {caracteristica.nome}
              </legend>

              <div className="mt-3 flex gap-6">
                <label className="flex min-h-11 items-center gap-2">
                  <input
                    type="radio"
                    name={caracteristica.id}
                    value="1"
                    required
                  />
                  Sim
                </label>

                <label className="flex min-h-11 items-center gap-2">
                  <input
                    type="radio"
                    name={caracteristica.id}
                    value="-1"
                  />
                  Não
                </label>
              </div>
            </fieldset>
          ))}

          <button
            type="submit"
            className="min-h-11 rounded-lg bg-emerald-800 px-5 font-semibold text-white"
            disabled={carregando}
          >
            {carregando ? "Classificando..." : "Classificar perfil"}
          </button>

          {erro && <p role="alert">{erro}</p>}

          {resultado && (
            <section
              aria-live="polite"
              className="rounded-2xl border border-stone-200 bg-stone-50 p-5"
            >
              <p className="text-sm font-semibold uppercase tracking-wide text-emerald-800">
                Resultado da classificação
              </p>

              <h2 className="mt-2 text-2xl font-bold text-stone-900">
                {resultado.perfil}
              </h2>

              <p className="mt-3 text-sm text-stone-600">
                Saída da rede neural:{" "}
                <span className="font-semibold text-stone-900">
                  {resultado.resposta}
                </span>
              </p>
            </section>
          )}
        </form>
      </section>
    </main>
  );
}