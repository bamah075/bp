import os
import anthropic
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-4-6"


class Agent:
    def __init__(self, name: str, role: str, task: str, output_path: str, system_prompt: str = ""):
        self.name = name
        self.role = role
        self.task = task
        self.output_path = output_path
        self.system_prompt = system_prompt or f"You are {name}, a {role}. Be thorough, specific, and produce high-quality work. When asked to save content, write it in full — never truncate or summarize."
        self.result: Optional[str] = None


class AgentRunner:
    def __init__(self, model: str = MODEL):
        self.client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
        self.model = model

    def run(self, agent: Agent, context: str = "") -> str:
        print(f"\n  [{agent.name}] Starting...")

        user_content = agent.task
        if context:
            user_content = f"Context from previous agents:\n\n{context}\n\n---\n\nYour task:\n{agent.task}"

        response = self.client.messages.create(
            model=self.model,
            max_tokens=8096,
            system=agent.system_prompt,
            messages=[{"role": "user", "content": user_content}],
        )

        result = response.content[0].text
        agent.result = result

        out = Path(agent.output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(result, encoding="utf-8")
        print(f"  [{agent.name}] Done → {agent.output_path}")
        return result

    def run_parallel(self, agents: list[Agent], shared_context: str = "") -> dict[str, str]:
        """Run multiple agents concurrently."""
        results: dict[str, str] = {}
        with ThreadPoolExecutor(max_workers=len(agents)) as executor:
            future_to_agent = {
                executor.submit(self.run, agent, shared_context): agent
                for agent in agents
            }
            for future in as_completed(future_to_agent):
                agent = future_to_agent[future]
                try:
                    results[agent.name] = future.result()
                except Exception as e:
                    print(f"  [{agent.name}] ERROR: {e}")
                    results[agent.name] = f"ERROR: {e}"
        return results

    def synthesize(self, task: str, context: str, output_path: str, role: str = "Synthesis Lead") -> str:
        """Run a synthesis/review pass after all agents finish."""
        agent = Agent(
            name="Synthesis Lead",
            role=role,
            task=task,
            output_path=output_path,
        )
        return self.run(agent, context=context)

    def share_findings(self, agents: list[Agent], findings_prompt: str) -> str:
        """Ask each agent to share their top findings, then compile."""
        findings = []
        for agent in agents:
            if agent.result:
                findings.append(f"### {agent.name}'s top findings\n{agent.result[:800]}...")
        return "\n\n".join(findings)
