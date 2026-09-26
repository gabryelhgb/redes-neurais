const caracteristicas = [
  { nome: "Raciocínio lógico", id: "raciocinio" },
  { nome: "Persistente", id: "persistente" },
  { nome: "Estudioso", id: "estudioso" },
  { nome: "Decidido", id: "decidido" },
];

export default function Home() {
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

        <form className="mt-8 space-y-5 rounded-2xl bg-white p-6 shadow-sm">
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
            type="button"
            className="min-h-11 rounded-lg bg-emerald-800 px-5 font-semibold text-white"
          >
            Classificar perfil
          </button>
        </form>
      </section>
    </main>
  );
}