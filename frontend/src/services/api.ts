import {
  AstronomicalObject,
  PaginatedObjects,
  DataQualityReport,
  SimulationScenarioHeader,
  SimulationResult,
  HohmannTransferResult,
  AIChatResponse,
  ResearchEvaluationResult,
  EvaluationTask,
  TaskRunResult,
  ScientificValidationSuiteReport,
  TelemetrySummary,
  UserMode
} from '../types/astronomy';

const API_BASE = '/api/v1';

export async function fetchObjects(category?: string, search?: string): Promise<AstronomicalObject[]> {
  const params = new URLSearchParams();
  if (category && category !== 'All') params.append('category', category);
  if (search) params.append('search', search);

  const res = await fetch(`${API_BASE}/objects/?${params.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch astronomical objects');
  const data = await res.json();
  return Array.isArray(data) ? data : (data.items || []);
}

export interface PaginatedQueryParams {
  page?: number;
  pageSize?: number;
  category?: string;
  search?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
  minMass?: number;
  maxMass?: number;
  minRadius?: number;
  maxRadius?: number;
  hasRings?: boolean;
  hasAtmosphere?: boolean;
}

export async function fetchPaginatedObjects(params: PaginatedQueryParams = {}): Promise<PaginatedObjects> {
  const q = new URLSearchParams();
  q.append('format', 'paginated');
  if (params.page) q.append('page', String(params.page));
  if (params.pageSize) q.append('page_size', String(params.pageSize));
  if (params.category && params.category !== 'All') q.append('category', params.category);
  if (params.search) q.append('search', params.search);
  if (params.sortBy) q.append('sort_by', params.sortBy);
  if (params.sortOrder) q.append('sort_order', params.sortOrder);
  if (params.minMass !== undefined) q.append('min_mass', String(params.minMass));
  if (params.maxMass !== undefined) q.append('max_mass', String(params.maxMass));
  if (params.minRadius !== undefined) q.append('min_radius', String(params.minRadius));
  if (params.maxRadius !== undefined) q.append('max_radius', String(params.maxRadius));
  if (params.hasRings !== undefined) q.append('has_rings', String(params.hasRings));
  if (params.hasAtmosphere !== undefined) q.append('has_atmosphere', String(params.hasAtmosphere));

  const res = await fetch(`${API_BASE}/objects/?${q.toString()}`);
  if (!res.ok) throw new Error('Failed to fetch paginated objects');
  return res.json();
}

export async function searchObjects(query: string, limit: number = 10): Promise<any> {
  const res = await fetch(`${API_BASE}/objects/search?q=${encodeURIComponent(query)}&limit=${limit}`);
  if (!res.ok) throw new Error('Search failed');
  return res.json();
}

export async function fetchObjectsByType(type: string): Promise<AstronomicalObject[]> {
  const res = await fetch(`${API_BASE}/objects/type/${encodeURIComponent(type)}`);
  if (!res.ok) throw new Error(`Failed to fetch objects of type '${type}'`);
  return res.json();
}

export async function fetchObjectById(id: string): Promise<AstronomicalObject> {
  const res = await fetch(`${API_BASE}/objects/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch object '${id}'`);
  return res.json();
}

export async function compareObjects(objectIds: string[], mode: UserMode = 'researcher'): Promise<any> {
  const res = await fetch(`${API_BASE}/compare/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ object_ids: objectIds, mode })
  });
  if (!res.ok) throw new Error('Failed to compare objects');
  return res.json();
}

export async function calculateHohmann(params: {
  origin_id?: string;
  target_id?: string;
  r1_au?: number;
  r2_au?: number;
}): Promise<HohmannTransferResult> {
  const res = await fetch(`${API_BASE}/calculate/hohmann`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate Hohmann transfer');
  return res.json();
}

export async function calculateHillSphere(params: {
  object_id?: string;
  semi_major_axis_au?: number;
  eccentricity?: number;
  body_mass_kg?: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/hill-sphere`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate Hill sphere');
  return res.json();
}

export async function calculateRocheLimit(params: {
  primary_radius_km: number;
  primary_density_g_cm3: number;
  secondary_density_g_cm3: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/roche-limit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate Roche limit');
  return res.json();
}

export async function calculateResonance(period1: number, period2: number): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/resonance`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ period_days_1: period1, period_days_2: period2 })
  });
  if (!res.ok) throw new Error('Failed to calculate orbital resonance');
  return res.json();
}

export async function calculateLagrangePoints(params: {
  primary_mass_kg?: number;
  secondary_mass_kg: number;
  separation_au: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/lagrange-points`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate Lagrange points');
  return res.json();
}

export async function fetchSimulationScenarios(): Promise<SimulationScenarioHeader[]> {
  const res = await fetch(`${API_BASE}/simulation/scenarios`);
  if (!res.ok) throw new Error('Failed to fetch scenarios');
  return res.json();
}

export async function fetchScenarioDetails(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/simulation/scenarios/${id}`);
  if (!res.ok) throw new Error('Failed to fetch scenario details');
  return res.json();
}

export async function runSimulation(params: {
  scenario_id: string;
  integrator?: string;
  total_time_years?: number;
  duration?: number;
  timestep?: number;
  num_steps?: number;
  selected_bodies?: string[];
}): Promise<SimulationResult> {
  const res = await fetch(`${API_BASE}/simulation/run`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error?.message || err.detail || 'Failed to run simulation');
  }
  return res.json();
}

export async function createSimulation(params: {
  scenario_id: string;
  duration?: number;
  timestep?: number;
  num_steps?: number;
  integrator?: string;
  selected_bodies?: string[];
  auto_run?: boolean;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/simulations`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.error?.message || err.detail || 'Failed to create simulation');
  }
  return res.json();
}

export async function getSimulation(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/simulations/${id}`);
  if (!res.ok) throw new Error(`Failed to fetch simulation ${id}`);
  return res.json();
}

export async function runSimulationById(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/simulations/${id}/run`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to run simulation ${id}`);
  return res.json();
}

export async function stopSimulation(id: string): Promise<any> {
  const res = await fetch(`${API_BASE}/simulations/${id}/stop`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to stop simulation ${id}`);
  return res.json();
}

export async function fetchSimulationsHistory(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/simulations`);
  if (!res.ok) throw new Error('Failed to fetch simulations history');
  return res.json();
}

export async function calculateGravityForce(params: {
  mass1_kg?: number;
  mass2_kg?: number;
  distance_m?: number;
  object1_id?: string;
  object2_id?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/gravity/force`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate gravitational force');
  return res.json();
}

export async function calculateSurfaceGravity(params: {
  mass_kg?: number;
  radius_m?: number;
  object_id?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/gravity/surface`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate surface gravity');
  return res.json();
}

export async function calculateOrbitalVelocity(params: {
  central_mass_kg?: number;
  radius_m?: number;
  semi_major_axis_m?: number;
  eccentricity?: number;
  object_id?: string;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/orbital-velocity`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate orbital velocity');
  return res.json();
}

export async function calculateOrbitalPeriod(params: {
  central_mass_kg?: number;
  orbiting_mass_kg?: number;
  semi_major_axis_m?: number;
  period1_s?: number;
  period2_s?: number;
}): Promise<any> {
  const res = await fetch(`${API_BASE}/calculate/orbital-period`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(params)
  });
  if (!res.ok) throw new Error('Failed to calculate orbital period');
  return res.json();
}



export async function chatAI(
  prompt: string,
  mode: UserMode,
  target_object_id?: string,
  history?: any[],
  simulation_id?: string,
  comparison_ids?: string[]
): Promise<AIChatResponse> {
  const res = await fetch(`${API_BASE}/ai/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      prompt,
      mode,
      target_object_id,
      simulation_id,
      comparison_ids,
      history
    })
  });
  if (!res.ok) throw new Error('Failed to get AI response');
  return res.json();
}

export async function fetchAIStatus(): Promise<any> {
  const res = await fetch(`${API_BASE}/ai/status`);
  if (!res.ok) throw new Error('Failed to fetch AI status');
  return res.json();
}

export async function fetchAITools(): Promise<any> {
  const res = await fetch(`${API_BASE}/ai/tools`);
  if (!res.ok) throw new Error('Failed to fetch AI tools');
  return res.json();
}

export async function evaluateResearch(
  query: string,
  target_object_id?: string
): Promise<ResearchEvaluationResult> {
  const res = await fetch(`${API_BASE}/research/evaluate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, target_object_id })
  });
  if (!res.ok) throw new Error('Failed to execute research evaluation');
  return res.json();
}

export async function fetchResearchHistory(): Promise<any[]> {
  const res = await fetch(`${API_BASE}/research/history`);
  if (!res.ok) throw new Error('Failed to fetch research history');
  return res.json();
}

export async function fetchResearchBenchmarks(): Promise<any> {
  const res = await fetch(`${API_BASE}/research/benchmarks`);
  if (!res.ok) throw new Error('Failed to fetch research benchmarks');
  return res.json();
}

export async function fetchDataStatus(): Promise<any> {
  const res = await fetch(`${API_BASE}/data/status`);
  if (!res.ok) throw new Error('Failed to fetch data status');
  return res.json();
}

export async function fetchDataQualityReport(): Promise<DataQualityReport> {
  const res = await fetch(`${API_BASE}/data/validate`);
  if (!res.ok) throw new Error('Failed to fetch data quality validation report');
  return res.json();
}

export async function syncDataSources(): Promise<any> {
  const res = await fetch(`${API_BASE}/data/sync`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to synchronize data sources');
  return res.json();
}

export async function fetchEvaluationTasks(): Promise<EvaluationTask[]> {
  const res = await fetch(`${API_BASE}/research/tasks`);
  if (!res.ok) throw new Error('Failed to fetch evaluation tasks');
  return res.json();
}

export async function startEvaluationTask(taskId: string): Promise<any> {
  const res = await fetch(`${API_BASE}/research/tasks/${taskId}/start`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to start task ${taskId}`);
  return res.json();
}

export async function completeEvaluationTask(
  taskId: string,
  payload: {
    session_id?: string;
    success: boolean;
    duration_ms?: number;
    metadata?: any;
  }
): Promise<any> {
  const res = await fetch(`${API_BASE}/research/tasks/${taskId}/complete`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error(`Failed to complete task ${taskId}`);
  return res.json();
}

export async function runAutomatedTask(taskId: string): Promise<TaskRunResult> {
  const res = await fetch(`${API_BASE}/research/tasks/${taskId}/run_automated`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to run automated task ${taskId}`);
  return res.json();
}

export async function runAllTasksAutomated(): Promise<any> {
  const res = await fetch(`${API_BASE}/research/tasks/run_all`, { method: 'POST' });
  if (!res.ok) throw new Error('Failed to run all automated tasks');
  return res.json();
}

export async function fetchScientificValidation(): Promise<ScientificValidationSuiteReport> {
  const res = await fetch(`${API_BASE}/research/validation/benchmarks`);
  if (!res.ok) throw new Error('Failed to fetch scientific validation benchmarks');
  return res.json();
}

export async function fetchTelemetrySummary(): Promise<TelemetrySummary> {
  const res = await fetch(`${API_BASE}/research/telemetry/summary`);
  if (!res.ok) throw new Error('Failed to fetch telemetry summary');
  return res.json();
}

export async function logTelemetryEvent(payload: {
  event_type: string;
  component?: string;
  duration_ms?: number;
  success?: boolean;
  metadata?: any;
}): Promise<any> {
  try {
    const res = await fetch(`${API_BASE}/research/telemetry`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    return res.json();
  } catch (err) {
    console.debug('Telemetry ingestion error', err);
  }
}

