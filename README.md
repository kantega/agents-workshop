# agents-workshop
Intro til Agentiske Systemer med AutoGen

## Installasjon
Lag et virtuelt miljø og installer avhengigheter. Bruk helst Python 3.13. For eksempel med bruk av `conda`:

```bash
conda create -n agents-workshop python=3.13
conda activate agents-workshop
pip install -r requirements.txt
```

Installer Docker med å følge instruksjonene på [docker.com](https://docs.docker.com/get-docker/).

Sørg for at Docker-tjenesten kjører, f.eks. med `sudo systemctl start docker`.

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

### Om AutoGen

AutoGen er et rammeverk utviklet av Microsoft for å bygge agentiske AI-systemer. Det tilbyr:

**Hovedfunksjoner:**
- **Multi-agent samtaler**: Agenter kan kommunisere i strukturerte diskusjoner
- **Rollespesialisering**: Hver agent kan ha spesifikke roller og ferdigheter
- **Fleksible arbeidsflyter**: Støtter både sekvensiell og parallell prosessering
- **Menneskelig integrasjon**: Kan inkludere mennesker i agent-diskusjoner
- **Kodegenerering og -kjøring**: Agenter kan skrive, kjøre og debugge kode

**Fordeler med AutoGen:**
- Enkel å sette opp og konfigurere
- Godt dokumentert og aktivt vedlikeholdt
- Støtter forskjellige LLM-er (OpenAI, Azure, lokale modeller)
- Innebygd støtte for kodeeksekverering og verktøybruk
- Fleksibel arkitektur som kan tilpasses mange bruksområder

### AutoGen Grunnleggende Konsepter

For å forstå hvordan AutoGen fungerer, er det viktig å kjenne til de grunnleggende byggesteinene:

#### Agenter (Agents)
Agenter er de grunnleggende enhetene i AutoGen som kan kommunisere og utføre oppgaver:

**AssistantAgent:**
- Standard AI-agent som bruker en språkmodell
- Kan ha spesialiserte systemmeddelelser for å definere rolle og oppførsel
- Kan utstyres med verktøy (tools) for utvidede funksjoner

**UserProxyAgent:**
- Representerer en menneskelig bruker i samtalen
- Kan be om input fra brukeren eller fungere automatisk
- Brukes for å integrere menneskelig vurdering i agent-arbeidsflyter

**CodeExecutorAgent:**
- Spesialisert agent for å kjøre kode
- Kan utføre kode i isolerte miljøer (som Docker-containere)
- Sikrer trygg eksekverering av generert kode

#### Teams og Kommunikasjonsmønstre
AutoGen organiserer agenter i team med definerte kommunikasjonsmønstre:

**RoundRobinGroupChat:**
- Agenter snakker i en forhåndsbestemt rekkefølge
- Hver agent får mulighet til å respondere i tur
- Enkelt å forstå og forutsigbart kommunikasjonsmønster

**Selector-baserte team:**
- Mer avanserte mønstre hvor en "selector" bestemmer hvem som skal snakke
- Kan tilpasse kommunikasjonsflyt basert på kontekst

#### Termineringsvilkår (Termination Conditions)
Definerer når en samtale eller oppgave skal avsluttes:

**TextMentionTermination:**
- Stopper når en spesifikk tekst nevnes (f.eks. "APPROVE")
- Nyttig for godkjenningsarbeidsflyter

**MaxMessageTermination:**
- Begrenser antall meldinger i en samtale
- Forhindrer uendelige diskusjoner

**Kombinerte vilkår:**
- Kan kombinere flere termineringsvilkår med logiske operatorer (AND/OR)

#### Modellklienter (Model Clients)
AutoGen støtter forskjellige språkmodeller gjennom modellklienter:

**AzureOpenAIChatCompletionClient:**
- Kobler til Azure OpenAI-tjenester
- Støtter modeller som GPT-4, GPT-4o, og GPT-4.1-nano
- Krever API-nøkkel og endpoint-konfigurasjon

**Konfigurasjon:**
```python
model_client = AzureOpenAIChatCompletionClient(
    azure_deployment="model-deployment-name",
    model="model-name",
    api_version="api-version" #"2024-10-21",
    azure_endpoint="https://your-azure-openai-endpoint.openai.azure.com/",
    api_key=api_key,
)
```

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
AutoGen bruker asynkron programmering for effektiv håndtering:

**Async/Await:**
- Alle AutoGen-operasjoner er asynkrone
- Tillater parallell prosessering og bedre ressursutnyttelse
- Krever `asyncio.run()` for å kjøre hovedfunksjoner

**Streaming:**
- Sanntidsvisning av agent-samtaler
- `Console` UI for å følge diskusjoner mens de pågår

### Hvordan kjøre Agenter og Teams

AutoGen tilbyr flere metoder for å kjøre agenter og teams, avhengig av om du vil ha sanntidsvisning eller bare resultatet:

#### Kjøring av Enkeltlagenter

**agent.run() - Enkel kjøring:**
```python
# Kjør en enkelt agent og få resultatet
result = await agent.run(task="Write a Python function to calculate fibonacci numbers")
print(result.messages[-1])  # Vis siste melding
```

**agent.run_stream() - Streaming kjøring:**
```python
# Kjør agent med sanntidsvisning
stream = agent.run_stream(task="Explain quantum computing")
await Console(stream)  # Vis meldinger mens de genereres
```

#### Kjøring av Teams

**team.run() - Team kjøring:**
```python
# Kjør et team og få alle meldinger
result = await team.run(task="Create a web application with HTML, CSS and JavaScript")
for message in result.messages:
    print(f"{message.source}: {message.content}")
```

**team.run_stream() - Team streaming:**
```python
# Kjør team med sanntidsvisning av diskusjonen
stream = team.run_stream(task="Design a database schema for an e-commerce system")
await Console(stream)  # Følg diskusjonen i sanntid
```

#### Praktiske Eksempler

**Enkelt Agent-Team:**
```python
import asyncio
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.ui import Console

async def main():
    # Opprett agenter
    coder = AssistantAgent("coder", model_client=model_client)
    reviewer = AssistantAgent("reviewer", model_client=model_client)
    
    # Opprett team
    team = RoundRobinGroupChat(
        participants=[coder, reviewer],
        termination_condition=MaxMessageTermination(6)
    )
    
    # Kjør oppgave
    task = "Write and review a Python function to sort a list"
    await Console(team.run_stream(task=task))

# Kjør hovedfunksjonen
asyncio.run(main())
```

**Med Menneskelig Interaksjon:**
```python
from autogen_agentchat.agents import UserProxyAgent

async def interactive_session():
    assistant = AssistantAgent("assistant", model_client=model_client)
    user_proxy = UserProxyAgent("user", input_func=input)
    
    team = RoundRobinGroupChat(
        [assistant, user_proxy],
        termination_condition=TextMentionTermination("DONE")
    )
    
    # Bruker kan delta i samtalen
    await Console(team.run_stream(task="Help me plan a Python project"))

asyncio.run(interactive_session())
```

#### Viktige Metoder og Konsepter

**team.reset():**
- Nullstiller teamets tilstand før ny oppgave
- Viktig å kalle mellom forskjellige oppgaver

```python
await team.reset()  # Nullstill før ny oppgave
result = await team.run(task="New task here")
```

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

#### Sikkerhet og Isolasjon
AutoGen har innebygde sikkerhetsfunksjoner:

**Docker-basert kodeeksekverering:**
- Isolerer kodekjøring fra hovedsystemet
- Forhindrer skadelig kode fra å påvirke vertsmaskinen
- Automatisk opprydding av ressurser

**Kontrollerte miljøer:**
- Definerte arbeidsmapper for hver oppgave
- Begrenset tilgang til systemressurser

### Arkitekturmønstre i AutoGen

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

## 🎯 Øvelsesrekkefølge

For å få mest mulig ut av workshoppen følger øvelsene en logisk progresjon fra enkle konsepter til mer avanserte multi-agent systemer. Anbefalt rekkefølge:

### 1. 🌐 Web Browsing med Verktøy
**Fil:** `web_browsing_exercise.py`  
**Konsepter:** Agent tools, funksjonskall, enkelt agent-system  
**Beskrivelse:** Lær hvordan du gir agenter tilgang til eksterne verktøy som web-søk. Øvelsen viser hvordan du definerer og bruker custom tools i AutoGen.

### 2. 💬 Agent-til-Agent Diskusjon  
**Fil:** `discussion_exercise.py`  
**Konsepter:** Multi-agent samtaler, RoundRobinGroupChat, termineringsvilkår  
**Beskrivelse:** Opprett ditt første multi-agent system hvor to agenter (primary og critic) diskuterer og forbedrer løsninger sammen. Introduserer peer review-mønsteret.

### 3. 👤 Interaktiv Diskusjon med Bruker
**Fil:** `discussion_with_user_exercise.py`  
**Konsepter:** UserProxyAgent, menneske-i-løkka, interaktive samtaler  
**Beskrivelse:** Utvid agent-systemet til å inkludere menneskelig input. Lær hvordan du integrerer brukerinteraksjon i agent-arbeidsflyter.

### 4. 🔧 Kodegenerering med Utførelse
**Fil:** `code_gen_2_agents.py`  
**Konsepter:** CodeExecutorAgent, Docker-isolasjon, kode-generering og testing  
**Beskrivelse:** Avansert øvelse som kombinerer kodegenerering og -utførelse. En agent skriver kode, en annen kjører den i et sikkert Docker-miljø.

---
**💡 Tips:** Start med øvelse 1 og arbeid deg oppover. Hver øvelse bygger på konseptene fra de forrige!
