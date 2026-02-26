# agents-workshop
Intro workshop til agentiske systemer med [Agent Framework](https://learn.microsoft.com/en-us/agent-framework/overview/?pivots=programming-language-python)

## Oppsett - jobbe lokalt på maskin eller i GitHub codespaces

- Clone dette repoet til din lokale maskin
- eller
- Bruk GitHub Codespaces

### Oppsett - jobbe lokalt på maskin

Anbefalt: Installere Visual Studio Code (https://code.visualstudio.com/download)

Alternativ: En annen valgfri IDE hvis du ønsker å kjøre python v3.13 der, alternativt kommandolinje.

```bash
# naviger til hvor du vil legge koden f.eks. ~/code/ eller C:\code
cd ~/code/

git clone https://github.com/kantega/agents-workshop.git

cd agents-workshop
```

- Installer `conda` (https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation), alternativt, `venv` eller lignende.
- Lag et virtuelt python 3.13-miljø via et miljøhåndteringsystem som `conda`, alternativt `venv`
- Installer nødvendige Python-pakker fra `requirements.txt` i ditt miljø. For eksempel med bruk av `conda`:

```bash
conda create -n agents-workshop python=3.13

conda activate agents-workshop

pip install -r requirements.txt

Cmd/Ctrl + Shift + P → Søk: Python Python: Select Interpreter → Conda: agents-workshop (3.13.11)
```
- Om du får feil: `CondaError: Run 'conda init' before 'conda activate'`, kjør `conda init` og start terminalen på nytt.

### Oppsett - jobbe i GitHub codespaces

> Alle GitHub-brukere skal ha minimum ~60 gratis timer kjøretid i Codespaces. 
> Det kan likevel hende en må legge til et betalingskort. 
> Bare spør hvis du lurer på noe i denne forbindelse.

> En kan [sette en grense](https://github.com/settings/billing/budgets) på f.eks. 3$ og beløpet gjelder ikke før grensen på ~60 gratis timer er nådd. 
> Etter 60 gratis timer påfølger kostnad på $0.18. [Les mer på codespaces](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces#pricing).

1. Naviger til https://github.com/kantega/agents-workshop
    - Eventuelt logg inn med din GitHub -bruker
2. Trykk `.` (dot)
3. `Run and debug (Cmd/Ctrl + Shift + D)` → Trykk på: `Continue working on ...`
4. Create New Codespace
    - Her kan du få en feilmelding, da det kan hende det ikke er knyttet en betaling til GitHub -konto 
5. Velg 2 cores ...
6. Codespaces har `Python 3.13` og `pip` forhåndsinstallert
    - basert på innholdet i .devcontainer/devcontainer.json
7. Åpne terminalen og installer pakker:

```bash
pip install -r requirements.txt
```

### Oppsett - Felles jobbe lokalt eller i GitHub codespaces

- Du får en API-nøkkel til Azure OpenAI-tjenesten fra oss. Opprett en `.env`-fil i prosjektmappen din (i root) og lim inn følgende i `.env`-filen:

```# .env
AZURE_OPENAI_API_KEY="din_api_nøkkel_her"
AZURE_OPENAI_ENDPOINT="https://kagents.openai.azure.com/"
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="gpt-5-nano"
AZURE_OPENAI_RESPONSES_DEPLOYMENT_NAME="gpt-5-nano"
```

- **Test at alt fungerer ved å kjøre `python test_environment.py`. Dette skriptet sjekker at alle nødvendige pakker er installert.**


## 🎯 Øvelsesrekkefølge

For å få mest mulig ut av workshoppen følger øvelsene en logisk progresjon fra enkle konsepter til mer avanserte multi-agent systemer. Anbefalt rekkefølge:

### 1. 🌐 Web Browsing med verktøy
**Fil:** `1_web_browsing_exercise.py`  
**Konsepter:** Agent tools, funksjonskall, enkelt agent-system  
**Beskrivelse:** Lær hvordan du gir agenter tilgang til eksterne verktøy som web-søk. Øvelsen viser hvordan du definerer og bruker custom tools i Agent Framework.

### 2. 💬 Agent-til-Agent diskusjon
**Fil:** `2_discussion_exercise.py`  
**Konsepter:** Multi-agent samtaler, Gruppe-chat i rekkefølge, termineringsvilkår  
**Beskrivelse:** Opprett ditt første multi-agent system hvor to agenter (primary og critic) diskuterer og forbedrer løsninger sammen. 

### 3. 👤 Interaktiv diskusjon med bruker
**Fil:** `discussion_with_user_exercise.py`  
**Konsepter:** requests, menneske-i-løkka, interaktive samtaler  
**Beskrivelse:** Utvid agent-systemet til å inkludere menneskelig input. Lær hvordan du integrerer brukerinteraksjon i agent-arbeidsflyter.

---

> **💡 Tips:** Start med øvelse 1 og arbeid deg nedover. Hver øvelse bygger på konseptene fra de forrige!

> Begynn gjerne på Oppgavene om du har kommet hit og vil starte på oppgavene.

Videre følgere litt teori og noen praktiske eksempler

## Om Agentiske Systemer

### Hva er agentiske systemer?
Agentiske systemer er AI-systemer som består av flere autonome agenter som kan samarbeide, kommunisere og koordinere sine handlinger for å løse komplekse oppgaver. I motsetning til tradisjonelle LLM-er som fungerer som enkeltstående modeller, kan agentiske systemer dele opp store problemer i mindre deler og la spesialiserte agenter håndtere hver del.

### Hvorfor bruker vi agentiske systemer?

**1. Kompleksitetshåndtering**
- Deler opp store, komplekse oppgaver i mindre, håndterbare deler
- Hver agent kan spesialisere seg på spesifikke domener eller funksjoner
- Reduserer kognitiv belastning på individuelle modeller

**2. Forbedret problemløsning**
- Flere perspektiver på samme problem gjennom forskjellige agenter
- Mulighet for iterativ forbedring gjennom agent-diskusjoner
- Selvkorreksjon og kvalitetssikring gjennom peer review

**3. Skalerbarhet og fleksibilitet**
- Enkelt å legge til nye agenter med spesialiserte ferdigheter
- Kan tilpasse systemet til forskjellige bruksområder
- Parallell prosessering av oppgaver

**4. Robusthet**
- Hvis en agent feiler, kan andre kompensere
- Redundans i systemet øker påliteligheten
- Bedre håndtering av edge cases

### Når er agentiske systemer anvendelige?

**Ideelle bruksområder:**
- **Komplekse forskningsoppgaver** som krever flere ekspertiseområder
- **Kodegenererering og -review** hvor forskjellige agenter kan fokusere på arkitektur, implementering og testing
- **Kreative prosesser** som krever brainstorming og iterativ forbedring
- **Beslutningsstøtte** hvor multiple perspektiver er verdifulle
- **Automatiserte arbeidsflyter** med flere trinn og avhengigheter

**Mindre egnet for:**
- Enkle, godt definerte oppgaver som kan løses av en enkelt modell
- Oppgaver med strenge latenskrav
- Situasjoner hvor ressursforbruk må minimeres

### Forskjeller fra "normale" LLM-er

| Aspekt | Tradisjonelle LLM-er | Agentiske Systemer |
|--------|---------------------|-------------------|
| **Arkitektur** | Enkelt modell-respons | Flere samarbeidende agenter |
| **Problemløsning** | Lineær, en-til-en | Iterativ, kollaborativ |
| **Spesialisering** | Generalist | Spesialiserte roller |
| **Kvalitetskontroll** | Begrenset selvkorreksjon | Peer review og validering |
| **Kompleksitet** | Begrenset av kontekstvindu | Kan håndtere større problemer |
| **Ressursbruk** | Lavere | Høyere (flere modellkall) |
| **Transparens** | Svart boks | Synlig diskusjon og resonnering |

### Om Agent Framework

Agent Framework er et rammeverk utviklet av Microsoft for å bygge agentiske AI-systemer. Det tilbyr:

**Hovedfunksjoner:**
- **Multi-agent samtaler**: Agenter kan kommunisere i strukturerte diskusjoner
- **Rollespesialisering**: Hver agent kan ha spesifikke roller og ferdigheter
- **Fleksible arbeidsflyter**: Støtter både sekvensiell og parallell prosessering
- **Menneskelig integrasjon**: Kan inkludere mennesker i agent-diskusjoner
- **Kodegenerering og -kjøring**: Agenter kan skrive, kjøre og debugge kode

**Fordeler med Agent Framework:**
- Enkel å sette opp og konfigurere
- Godt dokumentert og aktivt vedlikeholdt
- Støtter forskjellige LLM-er (OpenAI, Azure, lokale modeller)
- Innebygd støtte for kodeeksekverering og verktøybruk
- Fleksibel arkitektur som kan tilpasses mange bruksområder


> Oppdatering februar 2026:
Større oppdatering av workshop med migrering til Agent Framework

> Oppdatering oktober 2025:
AutoGen skal ikke utvikles videre (kun bugfix), siden Microsoft har lansert en ny plattform [Microsoft Agent Framework]("https://github.com/microsoft/agent-framework") som bygger videre på konseptene fra AutoGen og Semantic Kernel.

### Agent Framework - Grunnleggende konsepter

For å forstå hvordan Agent Framework fungerer, er det viktig å kjenne til de grunnleggende byggesteinene:

AzureOpenAIResponsesClient

#### Agenter
Agenter er de grunnleggende enhetene i Agent Framework som kan kommunisere og utføre oppgaver:

#### Teams og kommunikasjonsmønstre

Agent Framework organiserer agenter i team med definerte kommunikasjonsmønstre:

**Tur-basert:**
```
GroupChatBuilder(
    participants=[author, critic],
    orchestrator_agent=orchestrator
    ....
    # der orchestrator er instrueres til en tur-basert samtale.
```
Se også [forhåndsdefinert flyt](https://github.com/microsoft/agent-framework/blob/8e2cc4bedcf3ec0cf331f2f683d9884a0b72a7d7/python/samples/03-workflows/human-in-the-loop/agents_with_HITL.py#L201)

#### Modellklienter (Model Clients)
Agent Framework støtter forskjellige språkmodeller gjennom modellklienter:

**AzureOpenAIChatCompletionClient:**
- Kobler til Azure OpenAI-tjenester
- Støtter modeller som GPT-5, GPT-5o, og GPT-5-nano
- Krever API-nøkkel og endpoint-konfigurasjon

**AzureOpenAIResponsesClient:**
- Spesialisert klient for håndtering av strukturerte svar og responseparsing
- Integreres med Azure OpenAI for å formatere agentutput i henhold til definerte skjemaer
- Muliggjør typesikker responshandtering og validering i agent-arbeidsflyter


#### Verktøy (Tools)
Agenter kan utstyres med verktøy for å utføre spesifikke oppgaver:

**Egendefinerte funksjoner:**
- Python-funksjoner som agenter kan kalle
- Kan være synkrone eller asynkrone
- Må ha tydelige docstrings for at agenten skal forstå bruken

**Eksempel:**
```python
async def web_search(query: str) -> str:
    """Find information on the web"""
    # Implementasjon her
    return result
```

#### Arbeidsflyt og Eksekverering
Agent Framework støtter asynkron programmering for effektiv håndtering:

**Async/Await:**
- Alle Agent Framework-operasjoner er asynkrone
- Tillater parallell prosessering og bedre ressursutnyttelse
- Krever `asyncio.run()` for å kjøre hovedfunksjoner

### Hvordan kjøre Agenter og Teams

Agent Framework har flere metoder for å kjøre agenter og teams, avhengig av om du vil ha sanntidsvisning eller bare resultatet:

#### Kjøring av Enkeltlagenter

**agent.run() - Enkel kjøring:**
```python
# Kjør en enkelt agent og få resultatet
result = await agent.run(task="Write a Python function to calculate fibonacci numbers")
print(result.messages[-1])  # Vis siste melding
```

**agent.run(stream=True) - Streaming kjøring:**
```python
# Kjør agent med sanntidsvisning
stream = agent.run("Explain quantum computing", stream=True)
```

#### Kjøring av Team (Workflows)

**team.run() - Team kjøring:**
```python
# Kjør et team og få alle meldinger
result = await team.run(task="Create a web application with HTML, CSS and JavaScript")
for message in result.messages:
    print(f"{message.source}: {message.content}")
```

**team.run("stream=True) team streaming:**
```python
# Kjør team med sanntidsvisning av diskusjonen
stream = team.run(task="Design a database schema for an e-commerce system", stream=True)
await process_event_stream(stream)  # Følg diskusjonen i sanntid
...
```

#### Praktiske eksempler

**Streaming med output:**

```python
# Slå på intermediate_outputs for team
team = (
    GroupChatBuilder(
        ...
        intermediate_outputs=True
    ) ...

# kjør team workflow
team.run("Oppgave", stream=True)

...
# kombinert med process_event_stream.py:
async def process_event_stream(stream: AsyncIterable[WorkflowEvent]) -> dict[str, AgentRequestInfoResponse] | None:
    async for event in stream:
        if event.type == "output" and isinstance(event.data, AgentResponseUpdate):
            print(update.text, end="", flush=True) # print hvert token som output fra siste agent.
    ...
```

**Med Menneskelig Interaksjon:**
Håndtering av requests i stream events for å gi feedback til workflow-resultater. 

```python
# Get human input to steer the agent
user_input = input(f"Feedback for {request.executor_id} (or 'skip' to approve): ")
if user_input.lower() == "skip":
    user_input = AgentRequestInfoResponse.approve()
else:
    user_input = AgentRequestInfoResponse.from_strings([user_input])

responses[request_id] = user_input  
```

#### Viktige Metoder og Konsepter

**team (Workflow)**
- Er by default stateless og en kan kjøre en oppgave uten å tenke på resultatet fra forrige kjøring

**Håndtering av Resultater:**

```python
# Få tilgang til alle meldinger
result = await team.run(task="Some task")
for message in result.messages:
    print(f"Fra {message.source}: {message.content}")

# Få siste melding
last_message = result.messages[-1]
print(f"Siste svar: {last_message.content}")
```

**Feilhåndtering:**
```python
try:
    result = await team.run(task="Complex task")
    print("Oppgave fullført!")
except Exception as e:
    print(f"Feil under kjøring: {e}")
```

### Arkitekturmønstre i Agent Framework

**Peer Review-mønster:**
- En agent foreslår løsninger
- En annen agent evaluerer og gir tilbakemelding
- Iterativ forbedring til godkjenning

**Spesialist-mønster:**
- Forskjellige agenter har spesialiserte roller
- Koder, tester, dokumenterer, etc.
- Hver agent fokuserer på sitt ekspertiseområde

**Menneske-i-løkka-mønster:**
- Inkluderer menneskelig vurdering på kritiske punkter
- Kombinerer AI-effektivitet med menneskelig ekspertise
- Fleksibel kontroll over automatiseringsgrad

