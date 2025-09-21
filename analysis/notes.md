## Próximos Passos

1. Try different configs (see description bellow)

2. IBFT (por que é gambiarra? - roben)

 - Customizar diferentes estratégias de mudar o lider - medir impacto

 - Quando o lider falha o custo para trocar é alto. A troca proativa nao é tão custosa. Em tempo e tamanho de mensagem.

  - Ver como provocar a falha do líder

    - investigar diferentes protocolos e como lidam com essa estratégia da troca do líder

    - proativa vs

# Example Research Objectives for Analyzing BFT Protocols

Below are examples of evaluation questions and objectives that can guide experimental analysis of BFT protocols.

Students are expected to formulate hypotheses and design experiments to validate them.

---

### 1. Quorum Size and Latency Distribution

**Objective:**

Evaluate the impact of quorum size on performance under varying latency distributions.

**Questions:**

- How does a **larger quorum requirement** (phase reduction) compare to a **normal quorum** in terms of throughput and latency?

- Does performance degrade more severely as the number of processes and variance in latencies increase?

### 2. Scalability and Virtualization Effects

**Objective:**

Assess the scalability of BFT protocols when scaling to hundreds or thousands of nodes, with and without virtualization.

**Questions:**

- To what extent does **virtualization** (running multiple processes per physical node) impact experimental results?

- Which **bottlenecks** emerge under virtualization (CPU, memory, network)?

- If no bottlenecks are present, does virtualization preserve performance compared to physical deployments?
- 
### 3. Consensus Leadership Strategies

**Objective:**

Compare different leadership strategies in consensus protocols.

**Questions:**

- What is the **performance trade-off** between a **rotating leader** and a **fixed leader** (replaced only upon failure)?

- In networks with heterogeneous latencies, does rotating leadership degrade performance due to nodes with poor connectivity acting as leaders?

### 4. Responsiveness of Algorithms

**Objective:**

Quantify the impact of algorithmic responsiveness on fault tolerance and recovery.

**Questions:**

- How significant is the performance penalty of using **non-responsive algorithms** (i.e., slower leader replacement after failures)?

- Under fault scenarios, how does the speed of **view changes** affect throughput and latency?

### 5. Linear vs. Quadratic Communication Complexity

**Objective:**

Determine under which conditions linear-communication protocols (e.g., HotStuff) outperform quadratic protocols.

**Questions:**

- At what scale does **quadratic communication** (all-to-all messaging) become a practical bottleneck?

- How far can quadratic protocols **scale efficiently** before performance collapses?

- From which point is it preferable to adopt **linear communication protocols**, despite their higher latency per step (compensated via pipelining)?

### Final Step

**Students should formulate their own guiding question or hypothesis** to design experiments beyond these examples.