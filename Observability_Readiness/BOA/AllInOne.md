# BOA All-In-One Interview Prep

## Table of Contents

- [Must Be Smooth](#must-be-smooth)
  - [1.0 Walk me through how you built the capacity forecasting workflow.](#10-walk-me-through-how-you-built-the-capacity-forecasting-workflow)
  - [2.0 Why did you use Prophet for this forecasting work?](#20-why-did-you-use-prophet-for-this-forecasting-work)
  - [3.0 How do UCL testing, BreakPoint, TPS, and project assessment fit into capacity planning?](#30-how-do-ucl-testing-breakpoint-tps-and-project-assessment-fit-into-capacity-planning)
  - [11.0 How would you explain your role when the final action belongs to architecture, application owners, business owners, or infrastructure teams?](#110-how-would-you-explain-your-role-when-the-final-action-belongs-to-architecture-application-owners-business-owners-or-infrastructure-teams)
  - [12.0 How would you explain dashboards for this capacity process?](#120-how-would-you-explain-dashboards-for-this-capacity-process)
  - [21.0 What is your safest summary of the whole capacity forecasting project?](#210-what-is-your-safest-summary-of-the-whole-capacity-forecasting-project)
  - [22.0 Why should we hire you for this capacity role?](#220-why-should-we-hire-you-for-this-capacity-role)
- [Must Understand](#must-understand)
  - [4.0 How do clusters, load balancing, active/passive, and DR affect capacity planning?](#40-how-do-clusters-load-balancing-activepassive-and-dr-affect-capacity-planning)
  - [5.0 How do collection exceptions or missing metrics affect capacity planning?](#50-how-do-collection-exceptions-or-missing-metrics-affect-capacity-planning)
  - [6.0 How do business criticality, enterprise criticality, and franchise criticality affect capacity planning?](#60-how-do-business-criticality-enterprise-criticality-and-franchise-criticality-affect-capacity-planning)
  - [7.0 How do audit, governance, MCA, ServiceNow, and exception reporting fit into capacity planning?](#70-how-do-audit-governance-mca-servicenow-and-exception-reporting-fit-into-capacity-planning)
  - [8.0 What is the difference between a runbook and a playbook in this capacity process?](#80-what-is-the-difference-between-a-runbook-and-a-playbook-in-this-capacity-process)
  - [9.0 How do ESX hosts, VM guests, physical memory, virtual memory, and swap exceptions affect capacity planning?](#90-how-do-esx-hosts-vm-guests-physical-memory-virtual-memory-and-swap-exceptions-affect-capacity-planning)
  - [16.0 How would you explain vertical scaling vs horizontal scaling in this capacity planning process?](#160-how-would-you-explain-vertical-scaling-vs-horizontal-scaling-in-this-capacity-planning-process)
  - [17.0 How would you explain CPU thresholds and safety factors in capacity planning?](#170-how-would-you-explain-cpu-thresholds-and-safety-factors-in-capacity-planning)
  - [18.0 How would you handle collection exceptions, threshold exceptions, and ServiceNow follow-up without making it sound like just paperwork?](#180-how-would-you-handle-collection-exceptions-threshold-exceptions-and-servicenow-follow-up-without-making-it-sound-like-just-paperwork)
  - [19.0 How would you explain production-only capacity planning versus UAT or performance-test inputs?](#190-how-would-you-explain-production-only-capacity-planning-versus-uat-or-performance-test-inputs)
  - [20.0 How do you collaborate with application owners and architects on capacity decisions?](#200-how-do-you-collaborate-with-application-owners-and-architects-on-capacity-decisions)
- [Backup Only](#backup-only)
  - [10.0 How would you choose the right forecasting model or BMC forecast option for different applications?](#100-how-would-you-choose-the-right-forecasting-model-or-bmc-forecast-option-for-different-applications)
  - [13.0 How do you explain BMC TrueSight / TSCO / Helix in this capacity workflow without overclaiming?](#130-how-do-you-explain-bmc-truesight-tsco-helix-in-this-capacity-workflow-without-overclaiming)
  - [14.0 How would you handle a swap-space or memory-pressure exception?](#140-how-would-you-handle-a-swap-space-or-memory-pressure-exception)
  - [15.0 How do you explain SPECint or benchmark-style sizing in capacity planning without overclaiming?](#150-how-do-you-explain-specint-or-benchmark-style-sizing-in-capacity-planning-without-overclaiming)

## Must Be Smooth

## 1.0 Walk me through how you built the capacity forecasting workflow.
[Back to TOC](#table-of-contents)
Initially, a lot of the capacity forecast reporting relied on Excel-based
CBFR reports and BMC TrueSight capacity data. That worked, but it was not
efficient or repeatable enough as the reporting demand grew.

We already had a monthly capacity data pipeline, so the next step was to
evolve it into a more telemetry-focused forecasting workflow for the
applications and servers of interest.

The process started with telemetry extraction. We used extraction scripts,
including PL/SQL, to pull monthly capacity data from a mirror Oracle
database for BMC TrueSight. We also interfaced with CMDB data to bring in
application-related fields and ownership context.

Then I cleaned and normalized the data so joins were reliable and the time
series could be bucketed properly. That included timestamp normalization,
hourly and daily buckets, and grouping by host, application, and service.

After that, I engineered capacity features such as rolling averages,
rolling peaks, P95 values where useful, headroom to threshold, breach flags,
risk bands, and growth slope.

For forecasting, I used a time-based validation pattern. Train on an older
history window, such as 18 months, test against a more recent holdout window,
such as 6 months, compare forecasted values or risk bands against actual
outcomes, and adjust only when the backtest showed a real need.

Once the forecast looked reasonable, we used the full history to forecast
the next 3 to 6 month planning window.

The final output was not just a model. It became exception lists,
management summaries, dashboards, and CBFR-style planning outputs that
helped teams understand which applications or servers needed attention.


### Spine
1. Start with telemetry extraction.
2. Clean and normalize the data.
3. Bucket by time: hourly / daily.
4. Group by host, application, service.
5. Engineer capacity features.
6. Forecast and validate.
7. Publish dashboards, exception lists, and management summaries.

### Memory Line
It started as Excel/CBFR and TrueSight reporting, then evolved into a
repeatable telemetry pipeline with forecasting, validation, exception
lists, dashboards, and planning summaries.

## 2.0 Why did you use Prophet for this forecasting work?
[Back to TOC](#table-of-contents)

Prophet was part of the real forecasting work because capacity data is
time-series data, and we needed a practical way to handle trend and
seasonality.

It fit capacity planning needs without requiring a deep research-model
workflow. Some banking workloads have weekly rhythms, month-end effects,
quarter-end behavior, and other business-calendar patterns. A simple
straight-line forecast can miss those patterns.

Prophet helped model recurring behavior while keeping the output
explainable for engineers and leadership.

The goal was decision support, not deep ML research. We wanted to
identify capacity risk earlier and give teams more time to act.

Validation still mattered. I used holdout testing, compared forecasted
behavior against actual outcomes, and reviewed the output with SMEs
before trusting it for planning. 

### Memory Line
Prophet handled trend and seasonality, but the real value was
explainable decision support validated against actual behavior.

### Spine
1. Capacity data is time-series data.
2. It has trend and seasonality.
3. Some banking workloads have month-end, quarter-end,
   weekly, or business-calendar behavior.
4. Prophet was explainable enough for engineers and leadership.
5. The goal was decision support, not deep ML research.
6. Validation still mattered: holdout testing and SME review.

## 3.0 How do UCL testing, BreakPoint, TPS, and project assessment fit into capacity planning?
[Back to TOC](#table-of-contents)

UCL or BreakPoint-style testing gives a controlled view of throughput
limits, such as TPS capacity and saturation behavior.

When that information is available, I would treat it as an input to
the capacity playbook or runbook. Production telemetry shows the real
operating baseline, and the performance test tells us where the safe
upper range may be.

For application assessment, I would compare expected TPS or new volume
against the current production baseline, CPU thresholds, capacity pool
behavior, and safety margin.

If the application or cluster is approaching the safe limit, the
capacity team should notify stakeholders, application owners, and
architecture teams. The recommendation may be tuning, workload
redistribution, horizontal scaling, vertical scaling, or a planned
capacity add.

I would position the capacity team as advisory and evidence-driven.
We provide the view: current usage, tested limits, safety margin,
forecasted risk, and recommended options. The final action is usually
owned with the application, business, infrastructure, and architecture
teams.


### Spine 
1. Start with production baseline.
2. Add performance test / BreakPoint / UCL results.
3. Understand TPS and expected new volume.
4. Compare against CPU thresholds and safety margin.
5. Check capacity pool behavior.
6. Decide whether current capacity is enough.
7. Recommend tuning, horizontal scaling, vertical scaling,
   or planned capacity expansion.

### Memory line

Performance testing shows the limit, production telemetry shows where
we are, and project assessment decides whether new volume needs scaling.

## 11.0 How would you explain your role when the final action belongs to architecture, application owners, business owners, or infrastructure teams?
[Back to TOC](#table-of-contents)

The capacity planning team plays a pivotal role in stable and
cost-effective IT operations.

Our role is to monitor, alert, report, forecast, and advise. We collect
telemetry, create exception lists, build reports and dashboards, and
forecast where bottlenecks or savings opportunities may appear.

When it comes to final action, we are usually advisory. We provide the
evidence: baseline, utilization trend, headroom, TPS or volume context,
threshold risk, safety margin, forecast window, and recommended options.

The application owner, architecture team, infrastructure team, and
business owner usually own the final decision and implementation. That
may mean tuning, right-sizing, workload movement, horizontal scaling,
vertical scaling, capacity expansion, or accepting the risk with proper
documentation.

Our value is translating deep technical telemetry into business
language. Instead of only saying memory utilization is high, we explain
how much headroom remains, whether TPS growth is approaching a safe
limit, or whether the application may hit capacity in two months.

So the capacity team helps the business run smoothly, avoid production
risk, find savings where appropriate, and maintain documentation,
governance, follow-up, and closure. The communication has to stay open
until the issue is either remediated, accepted, or placed into a clear
action plan.


### Memory line
Capacity gives the view: evidence, risk, timing, and options.
Application, architecture, infrastructure, and business owners make and
execute the final decision.

### Spine 
1. Define your ownership: data, forecast, risk view, reporting.
2. Define stakeholder ownership: action and implementation.
3. Explain collaboration.
4. Mention evidence: baseline, threshold, headroom, forecast, TPS.
5. Mention options: tuning, right-sizing, horizontal/vertical scaling.
6. Mention follow-up: tickets, meetings, runbooks, closure.

### Points to hit

## 12.0 How would you explain dashboards for this capacity process?
[Back to TOC](#table-of-contents)

Dashboarding is one of the most powerful tools in capacity planning
because it becomes the communication layer between telemetry, forecasts,
and decisions.

A dashboard should not just show charts. It should help stakeholders
quickly understand where the baseline is, what the current trend looks
like, whether there is a sudden increase in utilization, how much
headroom remains, and when the forecast shows a system may approach
capacity.

It should also highlight the most critical applications first. A
manager, director, or business partner should be able to understand
the overall risk picture much faster than reading a long report.

At the same time, engineers should be able to drill down into the
details: application, service, cluster, host, metric, threshold,
forecast window, owner, exception status, and recommended action.

So I see dashboards as the decision view. They summarize capacity risk
for leadership, while still giving technical teams enough detail to
investigate and act.


### Memory line
A dashboard is the decision view: it shows risk, trend, headroom,
owner, timing, and action.
In short, dashboarding is how the capacity story becomes visible,
actionable, and easier to communicate.

### Spine 
1. Start with the purpose: decision support.
2. Show baseline/current trend.
3. Show forecast/risk window.
4. Show threshold/headroom/safety margin.
5. Show owner/application/criticality.
6. Show exception status/remediation status.
7. Make it usable for operations and leadership.

### Points to hit

## 21.0 What is your safest summary of the whole capacity forecasting project?
[Back to TOC](#table-of-contents)

Capacity forecast reporting started with Excel-based CBFR reports and
BMC TrueSight data. That was functional, but not scalable enough as
reporting demand grew.

We evolved an existing monthly data pipeline into a telemetry-driven
forecasting workflow. Extraction scripts, including PL/SQL, pulled
capacity data from a mirror Oracle database backing TrueSight, and we
joined CMDB data for application ownership context.

From there, the data was cleaned and normalized: timestamp alignment,
hourly and daily bucketing, and grouping by host, application, and
service.

Then we engineered capacity features: rolling averages, rolling peaks,
P95 utilization where useful, headroom to threshold, breach flags, risk
bands, and growth slope.

For forecasting, we used a time-based train/test approach: for example,
18 months to train and 6 months as a holdout to validate. We adjusted
only when the backtest showed a real need. Once the forecast was
reasonable, the full history supported a 3 to 6 month planning horizon.

The output went beyond a model. It became exception lists, management
summaries, dashboards, and CBFR-style planning reports that showed
which servers, applications, or capacity pools needed attention.

### Memory line

It started as Excel/CBFR and TrueSight reporting, evolved into a
telemetry-driven forecasting workflow, and ended as decision support:
exceptions, dashboards, and planning reports.

### Spine 
1. Started as reporting automation.
2. Evolved into telemetry-based forecasting.
3. Used SQL / Python / Pandas.
4. Prophet was real forecasting work.
5. Output was decision support.
6. Dashboards / CBFR-style reports / exception lists.
7. PySpark/Hadoop/cloud is scale-up path.
8. scikit-learn is lab modernization only.

### Points to hit

## 22.0 Why should we hire you for this capacity role?
[Back to TOC](#table-of-contents)

Honestly, this role is one of the closest matches to what I have
actually been doing.

At Citi, I worked around capacity planning for a large enterprise
banking environment: BMC TrueSight / TSCO-style data, PATROL agents,
CBFR-style reporting, Oracle-backed telemetry pipelines, and CMDB joins
for ownership context.

That is not just background knowledge for me. That is a workflow I
understand: production telemetry, baseline reports, thresholds,
exceptions, forecasts, dashboards, application owners, and management
summaries.

Banking capacity also has its own rhythm: critical applications,
governance, MCA or control-assessment pressure, audit evidence,
exception follow-up, and business owners who need technical risk
translated into clear action language. I am comfortable in that
environment.

Where I think I add value is that I can help modernize an Excel-heavy
reporting process without dismissing it. I understand why those reports
exist, but I can also help make them more repeatable with SQL, Python,
Pandas, validation checks, automated exception lists, and
dashboard-ready outputs.

I can also communicate the same capacity data at different levels:
technical detail for engineers, design impact for architects, and risk,
timing, ownership, and planning language for senior management.

BOA and Citi operate at similar banking scale with similar production
capacity pressures. I am not coming in to learn what capacity planning
is from zero. I am coming in as a ready contributor who can support the
team, strengthen the process, and help deliver the goals management has
set.

### Shorter version
This role fits my strongest background: enterprise banking capacity
planning, BMC-style telemetry, CBFR-style reporting, Python/Pandas
automation, KPI dashboards, forecasting, exception handling, and
stakeholder communication. I can meet the team where they are and help
modernize the process without losing the operational discipline that
banking capacity work requires.

### Memory line
I understand the current banking capacity workflow, and I can help make
it more repeatable, validated, dashboard-ready, and easier for leaders
to act on.

### Spine 
1. This role matches my strongest background.
2. I understand banking capacity and APM.
3. I understand BMC/TrueSight-style data.
4. I can improve Excel-heavy reporting into Python/Pandas workflows.
5. I can define KPIs, dashboards, and exception processes.
6. I can work with app owners, architects, and business teams.
7. I bring technical depth without losing business communication.

### Points to hit

## Must Understand

## 4.0 How do clusters, load balancing, active/passive, and DR affect capacity planning?
[Back to TOC](#table-of-contents)
Clustered applications provide resilience, but they also change the
capacity calculation.

Usually, servers may sit behind load balancers, and the architecture
can vary: round-robin load balancing, active/active, active/passive,
or disaster recovery design.

So for capacity planning, I would not simply add all servers together
and assume all capacity is freely available. The first question is:
how is traffic distributed, and what happens if one node or one site
goes down?

In an active/active design, I would look at total pool headroom and
also check whether any individual node is running hot. In an
active/passive design, I would not treat the passive node as normal
available capacity, because it may be reserved for failover.

For example, if the normal pool threshold is 70%, the per-node safety
threshold may need to be lower depending on how many nodes must absorb
load during failover. The exact number depends on the architecture and
the capacity standard of that organization.

The important point is that cluster capacity rules should be documented
in runbooks or playbooks: load-balancing behavior, failover assumption,
DR requirement, safety threshold, owner, and escalation path.

### Memory line
Cluster capacity is not simple addition. It depends on traffic
distribution, failover design, DR needs, and documented safety margin.

### Spine 
1. Start with architecture.
2. Identify the capacity pool or cluster.
3. Understand traffic distribution.
4. Separate active/active from active/passive.
5. Apply safety thresholds based on failover needs.
6. Consider DR and recovery scenarios.
7. Recommend action with architecture and app owners.


### Points to hit
Cluster:
A group of servers supporting the same application or function.

Load balancing:
Traffic may be distributed across nodes, often round-robin or based
on health/weight/capacity.

Active/active:
Multiple nodes serve production traffic at the same time.

Active/passive:
One node serves traffic, another is reserved for failover.

DR:
Disaster recovery requires enough spare or alternate capacity to run
the service if the primary site or node fails.

Safety threshold:
You cannot plan all nodes to run near 100%. You need reserve capacity
for spikes, failover, and business events.

Capacity pool:
The useful view is often pool-level capacity plus node-level exceptions.

## 5.0 How do collection exceptions or missing metrics affect capacity planning?
[Back to TOC](#table-of-contents)
A collection exception is a very important reporting signal for a
capacity planning team. The absence of telemetry is not the absence of
risk.

In a BMC TrueSight or Helix-style environment, agents or collection
feeds gather telemetry from servers and hosts. If the agent is down,
the mapping is wrong, or the feed is broken, the capacity report may
miss CPU, memory, storage, or other important metrics.

At Citi, we had exception reporting that compared the expected
server or application telemetry against what was actually collected.
If a server or application should have been reporting but was not, it
showed up as a collection exception.

Those exceptions need ownership and follow-up. The affected servers or
applications should be mapped to the appropriate business unit,
application owner, or infrastructure team. Based on the runbook or
playbook, the team should be alerted, ServiceNow tickets or requests
should be opened, and troubleshooting should be performed.

Until the metric collection is restored or the gap is explained, I
would flag that system in the capacity view. I would not treat missing
data as healthy capacity.


### Memory line
No telemetry does not mean no risk. It means the capacity view is not
trustworthy until the collection gap is resolved.

### Spine 
1. Define collection exception.
2. Explain why missing telemetry is dangerous.
3. Do not treat missing data as healthy.
4. Flag the system/report.
5. Notify or open issue with owning group.
6. Track through ServiceNow / weekly exception reporting.
7. Exclude or caveat the forecast until data quality is restored.

### Points to hit
Collection exception:
BMC/agent/feed did not collect expected data.

Examples:
- missing CPU
- missing memory
- stale host
- agent down
- wrong mapping
- broken feed
- VM/host not reporting
- timestamp gaps

Impact:
- dashboards may show incomplete picture
- forecast may understate risk
- audit/governance may require evidence
- owner team must be notified

## 6.0 How do business criticality, enterprise criticality, and franchise criticality affect capacity planning?
[Back to TOC](#table-of-contents)

Capacity planning is not the goal by itself. It is a vehicle for
protecting the business, maintaining operational stability, and
reducing cost where appropriate.

Criticality affects how much attention and safety margin an application
needs. A low-criticality system may tolerate normal monitoring and
planned remediation. A high-criticality, enterprise-critical, or
franchise-critical application needs earlier warning, tighter follow-up,
and faster owner engagement.

For example, more critical applications may receive more frequent CBFR
or capacity review attention, while less critical systems may be
reviewed on a lighter cycle. The same utilization number can mean a
different level of risk depending on the business impact.

Based on the runbook or playbook, higher-criticality applications may
have more conservative thresholds, stronger safety margins, faster
escalation, and more visibility to governance or audit teams.

So capacity risk is not only technical utilization. It is utilization
plus business criticality, ownership, timing, and operational impact.

### Memory line
Criticality changes the tolerance for risk, the escalation speed, and
the amount of safety margin we need.

### Spine 
1. Define criticality as business impact.
2. Explain low / medium / high criticality.
3. Explain enterprise-critical and franchise-critical.
4. Connect criticality to thresholds and safety margin.
5. Connect it to escalation and owner engagement.
6. Connect it to audit/governance visibility.

### Points to hit
Low criticality:
More tolerance, slower escalation.

Medium criticality:
Normal monitoring and planned remediation.

High criticality:
Tighter thresholds, faster owner engagement.

Enterprise critical:
Important across the enterprise; higher governance visibility.

Franchise critical:
Most sensitive / highest business impact; often treated as a subset
or top tier of enterprise-critical services.

Capacity impact:
Critical systems need earlier warning, stronger safety margin,
and more disciplined follow-up.

## 7.0 How do audit, governance, MCA, ServiceNow, and exception reporting fit into capacity planning?
[Back to TOC](#table-of-contents)

Governance and audit are a big part of banking operations. As a
capacity team, we support business partners by providing the evidence
they need to understand capacity risk, KPI exceptions, owner follow-up,
and remediation status.

For MCA or control-assessment style reporting, management may need to
see whether applications are missing certain capacity KPIs, crossing
thresholds, or having collection exceptions. That means the reporting
has to show what was detected, when it was detected, who owns it, and
what action is being taken.

We also support audit requests by retrieving historical evidence from
systems like BMC TrueSight or Helix, ServiceNow, dashboards, or other
capacity reports. That evidence helps show that risks were identified,
communicated, tracked, and resolved or accepted through the proper
process.

The goal is not just detection. The goal is traceability and closure:
detect the exception, notify the owner, track the action, and prove
that the issue was handled.

### Memory line
In banking capacity work, the report is not only a dashboard; it is
evidence of detection, ownership, action, and closure.

### Spine 
1. Capacity exceptions create governance evidence.
2. Reports show threshold breaches, collection gaps, and risks.
3. Owners are notified.
4. ServiceNow tickets or requests track the follow-up.
5. MCA / audit may review whether controls worked.
6. Historical BMC reports support evidence and traceability.
7. The goal is not just detection; it is closure.

### Points to hit

## 8.0 What is the difference between a runbook and a playbook in this capacity process?
[Back to TOC](#table-of-contents)
A runbook is the detailed step-by-step procedure for a known
operational situation.

For example, for a capacity threshold exception, the runbook tells the
engineer what to check: metric quality, host mapping, threshold,
owner, recent changes, and the recommended action path.

A playbook is broader. It describes the operating model: roles,
responsibilities, escalation points, governance rhythm, reporting
cadence, and how multiple runbooks are used together.

So in capacity work, the runbook guides a specific exception
investigation. The playbook describes how the overall capacity
operation runs across teams, reports, owners, governance, and closure.

### Memory line
The runbook tells the engineer what to do. The playbook tells the
organization how the process works.

### Spine 
1. Define runbook.
2. Define playbook.
3. Give capacity example.
4. Explain how they work together.
5. Connect to consistency, onboarding, and governance.

### Points to hit

## 9.0 How do ESX hosts, VM guests, physical memory, virtual memory, and swap exceptions affect capacity planning?
[Back to TOC](#table-of-contents)
For virtualized environments, I separate host-level capacity from
guest-level capacity.

The ESX host or cluster view tells us about the shared physical
resource pool: CPU pressure, memory pressure, contention, cluster
headroom, overcommitment, and physical capacity.

The VM guest view tells us about the application or server behavior:
CPU used, memory used, swap activity, service symptoms, and workload
demand.

Both views matter. A VM can look healthy while the underlying ESX host
or cluster is under pressure. Or the host can look fine while one VM is
constrained because of application behavior, memory pressure, or swap.

Virtualized resources also need careful interpretation. CPU can often
be shared more flexibly, but memory pressure is usually treated more
carefully because paging or swap can create performance problems.

If a VM moves between ESX hosts, I would not assume one cause
immediately. It could be normal balancing, maintenance, policy, or
resource pressure. But it is worth reviewing because movement can
affect capacity analysis and may reveal contention or cluster pressure.

So for capacity planning, I want both views: VM-level utilization and
host/cluster-level headroom.


### Memory line
In virtualization, capacity planning needs both views: the VM tells
you application behavior, and the ESX host tells you physical pool
pressure.

### Spine 
1. Separate host-level capacity from VM-level capacity.
2. ESX host shows physical pool pressure.
3. VM guest shows application/server behavior.
4. Physical vs virtual allocation matters.
5. Swap is an early warning signal.
6. Exception thresholds trigger review.
7. Action may be tuning, memory increase, VM movement,
   or cluster/pool adjustment.

### Points to hit

## 16.0 How would you explain vertical scaling vs horizontal scaling in this capacity planning process?
[Back to TOC](#table-of-contents)
Vertical scaling means adding more resources to an existing machine,
such as more CPU, memory, or storage.

Horizontal scaling means adding more machines or instances to a pool
or cluster so the workload can be shared across nodes.

Vertical scaling is often the quicker short-term option because it may
not require major application architecture changes. In a virtualized
environment, if resources are available, it may be handled through a VM
configuration change or planned resource increase.

Horizontal scaling is usually the stronger long-term pattern when the
application supports it. It works well for load-balanced or stateless
tiers because additional instances can share traffic. It can also
improve resilience, but the actual DR benefit depends on the failover
and site design.

The right decision depends on the workload, the application design,
criticality, expected TPS growth, current headroom, safety factor, and
cost/risk tradeoff.

As a capacity professional, my role is to provide the facts: baseline,
trend, threshold risk, forecast window, and options. Then I work with
business owners, application owners, architects, infrastructure teams,
and developers to decide whether tuning, vertical scaling, horizontal
scaling, or planned capacity expansion is the right path.

### Memory line
Vertical scaling makes the existing node bigger; horizontal scaling
adds more nodes. Capacity provides the evidence, and architecture
decides what pattern fits the application.

Sometimes vertical scaling is the bridge, and horizontal scaling is the
strategic fix.

### Spine 
1. Define vertical scaling.
2. Define horizontal scaling.
3. Explain when vertical scaling fits.
4. Explain when horizontal scaling fits.
5. Connect to project assessment and TPS.
6. Mention architecture/application owner decision.
7. Explain capacity team role: advisory evidence.

### Points to hit

## 17.0 How would you explain CPU thresholds and safety factors in capacity planning?
[Back to TOC](#table-of-contents)
A CPU threshold is the utilization level where we start treating the
system as approaching performance risk. A safety factor is the extra
buffer we keep so the system can absorb spikes, failover, batch load,
or unexpected demand.

We do not plan production systems to run at 100% utilization. If CPU is
pegged, work starts queuing, context switching can increase, latency
can rise, and the user experience or system stability can suffer.

For production and critical applications, the planning threshold is
usually more conservative. For example, some environments may use a
60-70% planning threshold, depending on the application, cluster
design, and capacity standard.

For clustered applications, the safety margin may need to be even more
careful because if one node or part of the cluster goes down, the
remaining nodes must absorb the load. So the threshold depends on
active/active, active/passive, load balancing, and DR assumptions.

When a system approaches the threshold, it should trigger a capacity
review. We check whether the behavior is a temporary spike, a batch
window, a business-calendar event, or sustained growth.

If it is sustained growth, we work with the application owner,
architecture team, and infrastructure team to decide whether the right
action is tuning, workload redistribution, vertical scaling,
horizontal scaling, or a planned capacity add before it impacts the
business.


### Memory line
A threshold is the warning line; a safety factor is the margin that
keeps production away from the cliff.

The goal is not to use every bit of capacity; the goal is to preserve
enough headroom for reliability, failover, and business spikes.

### Spine 
1. Define CPU threshold.
2. Define safety factor.
3. Explain why we do not plan to 100%.
4. Connect to business criticality.
5. Connect to clusters and failover.
6. Connect to project assessment / TPS growth.
7. Explain what happens when threshold is approached.

### Points to hit

## 18.0 How would you handle collection exceptions, threshold exceptions, and ServiceNow follow-up without making it sound like just paperwork?
[Back to TOC](#table-of-contents)
An exception is a break from the expected capacity baseline.

It can be a collection exception, where expected telemetry is missing,
or a threshold exception, where a KPI or metric is approaching or
breaching a safety threshold defined in the runbook or playbook.

These exceptions matter because they are early warning signals. Missing
telemetry does not mean the application is healthy; it means we may be
flying blind. And a threshold exception may mean the system is trending
toward performance or capacity risk.

When an exception appears, the first step is validation. I would check
whether the metric is real, whether the timestamp and mapping are
correct, and whether the behavior is a one-time spike, a known batch
window, a business-calendar event, or a sustained trend.

Once validated, I would map the infrastructure back to the application,
business unit, owner, manager, or support team using sources like CMDB
or service ownership data.

Then the appropriate owner is notified, and a ServiceNow ticket or
request can be opened if the runbook requires tracking. From there, the
issue should be followed to a decision, remediation, accepted risk, or
closure.

That is why I do not see exception reporting as paperwork. It turns a
technical finding into an owned action with evidence, visibility, and
accountability.


### Memory line
Exception reporting turns a finding into an owned action.
Losing telemetry does not mean the application is running fine; it
means we are flying blind.


### Spine 
1. Define exception.
2. Explain why it matters.
3. Validate the issue.
4. Map to owner/application/team.
5. Open or update ServiceNow if needed.
6. Track action and closure.
7. Report status to governance/management.

### Points to hit

## 19.0 How would you explain production-only capacity planning versus UAT or performance-test inputs?
[Back to TOC](#table-of-contents)
Production data shows how the application actually behaves under
real-world operating conditions. UAT and performance testing show how
the application behaves under controlled test conditions.

Most capacity teams focus heavily on production because production is
the source of truth. It includes real users, real batch cycles, real
business-calendar behavior, real contention, and real operational
constraints.

But UAT and performance testing are still very useful. They help us
understand controlled stress behavior, BreakPoint results, UCL-style
limits, and maximum TPS ranges before the application starts to show
risk.

I would not treat test results as a perfect copy of production. I
would treat them as sizing input. They help define safe operating
limits, safety factors, and additional KPIs or warning signals.

Then I compare those limits against production telemetry: current
baseline, trend, headroom, growth rate, and forecasted risk window.

So production tells us where we really are, while UAT and performance
testing help us understand how much safe room may remain before new
volume becomes risky.

### Memory line
Production tells us where we are. UAT and performance testing help
estimate the safe upper range. Capacity planning uses both with safety
margin.
Performance-test KPIs can become early warning signals so the business
can act before production hits a usage bottleneck.

### Spine 
1. Production is the source of real operating behavior.
2. UAT/performance testing gives controlled test signals.
3. BreakPoint/UCL/TPS helps estimate limits.
4. Production telemetry confirms actual usage and trend.
5. Do not blindly copy UAT behavior into production assumptions.
6. Use safety factors.
7. Work with app owners and architecture for final sizing.

### Points to hit

## 20.0 How do you collaborate with application owners and architects on capacity decisions?
[Back to TOC](#table-of-contents)
Capacity planning works best as a partnership model.

My role is to bring evidence: baseline trend, headroom, threshold risk,
forecasted window, and safety margin. Then I align that with application
owners, architects, infrastructure teams, and business stakeholders.

If risk is rising, we review options together: tuning, workload shift,
right-sizing, vertical or horizontal scaling, or planned capacity add.

So I position capacity as advisory and decision-support focused. We provide
clear risk language and recommended options, then partner with owners on final
implementation and timing.

### Memory line
Capacity provides the evidence, and owners plus architects help choose the
right action path.

### Spine
1. Start with evidence.
2. Translate risk into business impact and timing.
3. Review options with owners and architects.
4. Align on action and ownership.
5. Track follow-up and closure.

### Points to hit

## Backup Only

## 10.0 How would you choose the right forecasting model or BMC forecast option for different applications?
[Back to TOC](#table-of-contents)
The question is not specific to BMC alone. It applies to any
forecasting tool. The main idea is fit: choose the model that matches
the behavior of the application or capacity pool.

I would not start by running one forecast across thousands of mixed
servers. First, I would group systems into cohorts based on function,
ownership, workload pattern, criticality, and business behavior.

Then I would start with a smaller, controlled set of systems in a
cohort and compare reasonable forecasting options. Depending on the
tool, that might include simple trend, linear or polynomial-style
models, exponential behavior, or seasonality-aware models.

The validation step is key. I would split known telemetry into a
training window and a holdout testing window. Then I would compare the
forecast against actual behavior, thresholds, risk bands, and SME
feedback.

If one model or configuration performs best for that cohort, I would
use it for that cohort, not blindly for every application. If behavior
changes over time, I would retest and adjust.

So the model choice is driven by workload behavior and validation, not
by choosing the fanciest option. 

### Memory line

### Spine 
1. Start with workload behavior.
2. Check whether the app is steady, growing, seasonal, batch-heavy,
   or noisy.
3. Use simple models where simple models work.
4. Use seasonality-aware forecasting where patterns repeat.
5. Clean noisy data before trusting a model.
6. Validate with holdout testing and SME review.
7. Choose the model that improves decision quality, not the fanciest one.

### Points to hit

## 13.0 How do you explain BMC TrueSight / TSCO / Helix in this capacity workflow without overclaiming?
[Back to TOC](#table-of-contents)

At Citi, BMC TrueSight / TSCO-style tooling was very familiar territory.
Our team worked closely with that ecosystem for capacity data, reporting,
forecasting, and exception analysis.

I would not position myself as the sole BMC platform administrator. My
strongest role was on the capacity and reporting side: using the collected
telemetry to create baseline reports, identify exceptions, support forecasts,
and turn the data into planning views.

At a high level, the workflow is agent or feed based. Agents or adapters collect
host, device, infrastructure, and in some cases cloud-related metrics. That data
is processed, normalized, enriched, and stored so it can support reporting,
dashboarding, exception tracking, and forecasting.

For heavy reporting, it is common to work against reporting or replicated data
stores rather than disturbing the operational system. From there, capacity teams
can query historical data, review trends, run forecast models, and build reports
or dashboards for application owners and leadership.

The important point is not only the tool name. The value is the workflow:
collect reliable telemetry, validate collection quality, map it to applications
and owners, define KPIs and thresholds, run forecasts, flag exceptions, and
support capacity decisions.

So I am comfortable with BMC TrueSight / TSCO-style capacity environments, and
if Helix is part of the current stack, I would treat it as related BMC ecosystem
context and confirm the exact implementation before overclaiming details.

### Memory line

### Spine 
1. TrueSight / TSCO are familiar capacity tools.
2. They support production telemetry, baseline reporting,
   thresholds, and forecasting.
3. BMC agents / feeds collect data from hosts.
4. Collection quality matters.
5. Helix may be related BMC operations context, but learn exact usage.
6. Do not make the answer only about the tool.
7. Bring it back to capacity process and decision support.

### Points to hit

## 14.0 How would you handle a swap-space or memory-pressure exception?
[Back to TOC](#table-of-contents)
When I see a swap-space or memory-pressure exception, the first thing
I do is validate whether it is a real event or a temporary blip. I look
at the metric, the timestamp, the host or VM mapping, and whether it is
a one-time spike or something building over time.

Then I gather system context. Is this a physical host, a VM, or a
container? What application or workload is running on it? A scheduled
batch job at 2 a.m. looks very different from a production application
server where memory usage has been creeping up for two weeks.

Next, I check history. Has this system hit the limit before? Is it
trending toward a threshold? Was there a recent deployment or workload
change? That helps separate a true capacity issue from an application
issue, bad deployment, or one-time operational event.

If it is a temporary spike, I would notify or document as needed and
continue monitoring. If it is sustained, then it becomes a capacity
conversation.

The options could include JVM or application tuning, right-sizing the
VM, moving workload off the host, increasing memory, or scheduling a
planned capacity change before it becomes an incident.

The main goal is to get ahead of the issue. Swap activity is a symptom,
not the disease. By the time a system is swapping heavily, the early
warning signs may already have been missed, so I focus on trend,
headroom, and sustained behavior rather than waiting only for a hard
threshold alert.

### Memory line
Swap is a symptom, not the disease. Validate it, understand the
context, check the trend, then choose tuning, movement, right-sizing,
or capacity expansion.

### Spine 
1. Define the exception.
2. Validate the metric and timestamp.
3. Check host/VM/application context.
4. Compare against threshold and history.
5. Determine if it is spike or sustained trend.
6. Notify owner / open ticket if needed.
7. Recommend tuning, memory increase, workload movement, or monitoring.

### Points to hit

## 15.0 How do you explain SPECint or benchmark-style sizing in capacity planning without overclaiming?
[Back to TOC](#table-of-contents)
SPECint gives us a common way to compare CPU performance across
different hardware generations.

Raw CPU percentage alone can be misleading. A server running at 70%
CPU on an older small physical machine is not the same capacity as
70% CPU on a newer larger server or cloud instance.

So benchmark-style sizing helps normalize the comparison. It gives us
a way to estimate how much compute capacity a workload may need during
a hardware refresh, consolidation, or migration.

But I would not use benchmark math alone as the final answer. SPECint
or vendor benchmark scores are measured under controlled conditions.
Production has memory pressure, IO wait, network latency, virtualization
overhead, noisy neighbors, batch windows, and business demand patterns.

So I treat the benchmark as a starting point for sizing. Then I combine
it with real telemetry: CPU trend, peaks, utilization history, TPS,
headroom, and safety margin.

After migration or resizing, I would validate again against actual
production behavior and adjust if needed.

### Memory line
Benchmark sizing gives a normalized view of compute capacity, but
production telemetry tells us how the application actually behaves.
Use the benchmark to frame the sizing conversation, and use telemetry
to make and validate the actual capacity decision.

### Spine 
1. Define the purpose: normalize hardware capacity.
2. Explain why raw CPU percent is not enough.
3. Connect benchmark capacity to sizing and comparison.
4. Use it with telemetry, not instead of telemetry.
5. Keep the answer practical and advisory.
6. Do not pretend benchmark math alone gives the final answer.

### Points to hit
