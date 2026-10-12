# Cleaned Data Summary

This document provides a comprehensive structural and statistical overview of the datasets located in the [`Cleaned Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data) directory.

---

## 1. Overview & Timespan

- **Source Directory:** [`Cleaned Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data)
- **Time Horizon:** **January 27, 2026 – July 26, 2026**
- **Duration:** **181 Calendar Days** (~6 full months)
- **Data Integrity:** **0 null or missing values** across all records in all datasets.
- **Naming Pattern:** `YYYY-MM-DD_<category_slug>.csv`

---

## 2. Subfolder Comparison & Missing Dates

| Subfolder | File Count | Date Range | Total Span (Days) | Missing Dates | Total Rows | Null Values |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| [Energy Data](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Energy%20Data) | **180** | 2026-01-27 to 2026-07-26 | 181 | **`2026-03-01`** (1 day) | 1,980 | 0 |
| [Load Curve](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Load%20Curve) | **181** | 2026-01-27 to 2026-07-26 | 181 | **None** (100% complete) | 17,195 | 0 |
| [Night Peak Data](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Night%20Peak%20Data) | **181** | 2026-01-27 to 2026-07-26 | 181 | **None** (100% complete) | 2,172 | 0 |
| [Peak Data](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Peak%20Data) | **180** | 2026-01-27 to 2026-07-26 | 181 | **`2026-03-01`** (1 day) | 542 | 0 |
| [Reservoir Data](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Reservoir%20Data) | **181** | 2026-01-27 to 2026-07-26 | 181 | **None** (100% complete) | 2,172 | 0 |

> **Note on `2026-03-01`:**
> The source raw files [`data/gensum/energy_data/2026-03-01.csv`](file:///d:/GiTHuB/Power-Management-Study/data/gensum/energy_data/2026-03-01.csv) and [`data/gensum/peak_data/2026-03-01.csv`](file:///d:/GiTHuB/Power-Management-Study/data/gensum/peak_data/2026-03-01.csv) are empty files in the raw data (0–2 bytes). In contrast, `Load Curve`, `Night Peak Data`, and `Reservoir Data` contain complete data for `2026-03-01`.

---

## 3. Subfolder Details & Column Schemas

### 3.1. Energy Data
- **Location:** [`Cleaned Data/Energy Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Energy%20Data)
- **Description:** Aggregated daily total electrical energy generated (in Gigawatt-hours) across Ceylon Electricity Board (CEB) and Independent Power Producer (IPP) power plants and technologies.
- **Granularity:** Daily summary (1 record per station group per day, with timestamp `YYYY-MM-DDT23:59:59`).
- **Rows per File:** 11 rows.
- **Columns:**
  - `stationGroupName` (*string*): Power station complex / generation category.
  - `energyGWh` (*float*): Total energy generated on that day in GWh.
  - `dateTime` (*string*): ISO 8601 timestamp (`YYYY-MM-DDT23:59:59`).
- **Tracked Station Groups (11):**
  - Laxapana Complex
  - Mahaweli Complex
  - Samanala Complex
  - CEB Thermal - Coal
  - CEB Thermal - Oil
  - IPP Thermal
  - CEB Wind
  - IPP Wind
  - IPP Solar
  - IPP BMP (Biomass Power)
  - IPP MHP (Mini Hydro Power)

---

### 3.2. Load Curve
- **Location:** [`Cleaned Data/Load Curve/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Load%20Curve)
- **Description:** High-resolution electrical power dispatch curves across the Sri Lankan national grid.
- **Granularity:** 15-minute intervals from `00:15:00` to `23:45:00` (95 intervals/day).
- **Rows per File:** 95 rows.
- **Columns:**
  - `DateTime` (*string*): Timestamp in `YYYY-MM-DD HH:MM:SS` format.
  - `Wind` (*float*): Total wind power in MW.
  - `SPP Biomass` (*float*): Small Power Producer Biomass in MW.
  - `Thermal-Oil` (*float*): Heavy fuel oil / diesel thermal generation in MW.
  - `Major Hydro` (*float*): Major reservoir hydroelectric generation in MW.
  - `Coal` (*float*): Lakvijaya Coal power generation in MW.
  - `Solar` (*float*): Grid-connected solar generation in MW.
  - `SPP Minihydro` (*float*): Small Power Producer run-of-river mini hydro in MW.

---

### 3.3. Night Peak Data
- **Location:** [`Cleaned Data/Night Peak Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Night%20Peak%20Data)
- **Description:** Power dispatch breakdown during the system night peak demand window (7:00 PM / `19:00:00`).
- **Granularity:** Snapshot at `19:00:00` daily.
- **Rows per File:** 12 rows.
- **Columns:**
  - `stationGroupName` (*string*): Generation complex, technology group, or reactive support.
  - `activePowerMW` (*float*): Real power delivered at peak in MW.
  - `reactivePowerMvar` (*float*): Reactive power supplied/absorbed in Mvar.
  - `dateTime` (*string*): ISO 8601 timestamp (`YYYY-MM-DDT19:00:00`).
- **Tracked Station Groups (12):**
  - Laxapana Complex
  - Mahaweli Complex
  - Samanala Complex
  - CEB Thermal - Coal
  - CEB Thermal - Oil
  - IPP Thermal
  - CEB Wind
  - IPP Wind
  - CEB Small Hydro
  - IPP BMP
  - IPP MHP
  - Capacitors

---

### 3.4. Peak Data
- **Location:** [`Cleaned Data/Peak Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Peak%20Data)
- **Description:** Grid-wide load snapshots during the primary daily operational regimes: Day Peak, Night Peak, and Off-Peak.
- **Granularity:** Snapshot for each demand regime (typically 3 rows/day: Off Peak around 03:00–04:00, Day Peak around 12:00–16:45, Night Peak around 19:00–19:15).
- **Rows per File:** 3 rows (except `2026-03-02`, which has 5 rows due to multiple peak intervals recorded).
- **Columns:**
  - `stationGroupName` (*string*): Peak regime identifier (`Day Peak`, `Night Peak`, `Off Peak`).
  - `activePowerMW` (*float*): Grid total active power demand in MW.
  - `reactivePowerMvar` (*float*): Grid total reactive power in Mvar.
  - `dateTime` (*string*): Exact time of peak occurrence.

---

### 3.5. Reservoir Data
- **Location:** [`Cleaned Data/Reservoir Data/`](file:///d:/GiTHuB/Power-Management-Study/Cleaned%20Data/Reservoir%20Data)
- **Description:** Daily hydrological and storage parameters of major hydroelectric reservoirs in Sri Lanka.
- **Granularity:** Daily morning observation (typically `06:00:00`).
- **Rows per File:** 12 rows.
- **Columns:**
  - `reservoirName` (*string*): Name of the hydro reservoir.
  - `rainfallmm` (*int/float*): 24-hour recorded catchment rainfall in millimeters.
  - `storagePercentage` (*float*): Usable water storage level as a percentage of total capacity.
  - `waterLevel` (*float*): Reservoir water elevation (m / ft MSL).
  - `dateTime` (*string*): ISO 8601 timestamp (`YYYY-MM-DDT06:00:00`).
- **Tracked Reservoirs (12):**
  - Castlereigh
  - Maussakalle
  - Kotmale
  - Victoria
  - Randenigala
  - Samanalawewa
  - Inginiyagala
  - Ukuwela
  - Rantambe
  - Bowatenna
  - Kukule
  - Upper Kothmale (Upper Koth.)
