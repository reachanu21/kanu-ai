from openclaw import Agent, Ollama, Memory

llm = Ollama(model="llama3.2")
memory = Memory()
agent = Agent(llm=llm, memory=memory)

print(agent.run("Hello, who are you"))
