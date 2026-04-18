---
name: Reference — Public Research Data Sources
description: Validated public data sources for energy, carbon, and AI workload research. Tested and used in ai-energy-ot project.
type: reference
---

## Carbon Intensity
- **WattTime MOER:** 345 US regions, hourly marginal operating emissions rate, multi-year. Free for research via gridemissionsdata.io. Best source for marginal emissions.
- **EPA eGRID:** 27 subregions, annual static emissions factors. Free at epa.gov/egrid. Good for baselines, not time-varying analysis.
- **ElectricityMaps:** Real-time + historical average CI. Free tier real-time only; academic access needed for historical.

## AI Workload Traces
- **Azure LLM Inference Traces 2023:** 28K requests (code + conversation), timestamps + token counts. CC-BY-4.0. Citation: Patel et al. "Splitwise", ISCA 2024.
- **Google Cluster Traces 2019:** Borg workload + power traces, 57 power domains. Free via BigQuery (2.4 TiB). Very large.

## Latency
- **Azure Inter-Region RTT:** 50x50 Azure regions, P50 ms. From Microsoft networking docs.

## Grid Models
- **PyPSA-USA:** Open-source US power system model (WECC, ERCOT, Eastern). MIT license.

## Environmental Justice
- **EPA EJScreen:** Census block group level. Archived on Zenodo (zenodo.org/records/14767363) after EPA removed in Feb 2025.

## Key Gotcha
EPA/government download URLs sometimes redirect to HTML error pages. Always check downloaded file size — if it's ~6KB, you got an error page, not data. May need manual download.
