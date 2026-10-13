export type UserMode = 'citizen' | 'student' | 'researcher';

export interface SourceMetadata {
  source_name: string;
  source_url?: string | null;
  retrieval_date?: string | null;
  is_demo_seed: boolean;
  confidence_level: string;
  provenance_badge: string;
}

export interface AstropyUnitsBreakdown {
  mass_solar?: number | null;
  mass_jupiter?: number | null;
  mass_earth?: number | null;
  radius_solar?: number | null;
  radius_jupiter?: number | null;
  radius_earth?: number | null;
  distance_au?: number | null;
  distance_parsec?: number | null;
  distance_light_years?: number | null;
  surface_gravity_gees?: number | null;
  temperature_celsius?: number | null;
}

export interface RelatedObjectSummary {
  id: string;
  name: string;
  category: string;
  relationship: string;
  color_hex?: string;
}

export interface AstronomicalObject {
  id: string;
  name: string;
  category: 'Planet' | 'Star' | 'Exoplanet' | 'Moon' | 'Deep-Sky' | 'Asteroid' | 'Comet' | string;
  parent_body_id?: string | null;
  
  // Physical parameters
  mass_kg?: number | null;
  mass_earth_relative?: number | null;
  radius_km?: number | null;
  radius_earth_relative?: number | null;
  mean_density_g_cm3?: number | null;
  surface_gravity_m_s2?: number | null;
  escape_velocity_km_s?: number | null;
  surface_temperature_k?: number | null;
  luminosity_solar?: number | null;
  spectral_type?: string | null;
  apparent_magnitude?: number | null;
  absolute_magnitude?: number | null;

  // Orbital parameters
  semi_major_axis_au?: number | null;
  eccentricity?: number | null;
  orbital_inclination_deg?: number | null;
  orbital_period_days?: number | null;
  perihelion_au?: number | null;
  aphelion_au?: number | null;
  mean_orbital_velocity_km_s?: number | null;
  orbital_velocity?: number | null;
  rotation_period?: number | null;
  rotation_period_hours?: number | null;
  distance_from_sun?: number | null;
  object_type?: string;
  source?: string;
  source_url?: string | null;
  units?: Record<string, string>;
  metadata?: Record<string, any>;

  // Visual
  color_hex?: string;
  texture_preset?: string;
  has_rings?: boolean;
  has_atmosphere?: boolean;

  // Adaptive content
  description?: string;
  description_citizen: string;
  description_student: string;
  description_researcher: string;
  educational_facts?: string[];
  research_notes?: Record<string, any>;

  // Provenance & Source Transparency
  data_source?: string;
  data_confidence?: string;
  source_metadata?: SourceMetadata;

  // Astropy & Related Bodies
  astropy_units?: AstropyUnitsBreakdown;
  related_objects?: RelatedObjectSummary[];

  // Computed 3D orbit line
  orbit_path_3d?: number[][];
}

export interface PaginatedObjects {
  items: AstronomicalObject[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
}

export interface FieldValidationIssue {
  field: string;
  issue_type: 'error' | 'warning' | 'info';
  message: string;
  value?: any;
}

export interface ObjectValidationResult {
  object_id: string;
  name: string;
  category: string;
  is_valid: boolean;
  issues: FieldValidationIssue[];
  physical_consistency_score: number;
}

export interface DataQualityReport {
  total_objects_inspected: number;
  objects_valid: number;
  objects_with_warnings: number;
  total_errors: number;
  total_warnings: number;
  quality_score_percent: number;
  units_validated: string[];
  object_results: ObjectValidationResult[];
}

export interface SimulationScenarioHeader {
  id: string;
  name: string;
  description: string;
  mode_focus: string;
  body_count: number;
  default_time_years: number;
  recommended_integrator: string;
  assumptions?: string[];
  units?: Record<string, string>;
  bodies?: Array<{
    id: string;
    name: string;
    mass: number;
    color: string;
    radius_km?: number;
    radius_display?: number;
    x: number;
    y: number;
    z: number;
    vx: number;
    vy: number;
    vz: number;
  }>;
}

export interface SimulationBodyState {
  id: string;
  name: string;
  mass: number;
  color: string;
  radius_km?: number;
  radius_display?: number;
  initial_position?: [number, number, number];
  initial_velocity?: [number, number, number];
  final_position: [number, number, number];
  final_velocity: [number, number, number];
  positions?: [number, number, number][];
  velocities?: [number, number, number][];
  speeds?: number[];
  distances_from_center?: number[];
  trajectory: [number, number, number][];
}

export interface SimulationPairwiseDistance {
  pair_id: string;
  pair_name: string;
  body1_id: string;
  body2_id: string;
  min_distance: number;
  max_distance: number;
  series: Array<{
    time: number;
    distance: number;
  }>;
}

export interface SimulationResult {
  scenario_name?: string;
  engine_used: string;
  integrator: string;
  runtime_ms: number;
  steps_computed: number;
  total_time_years: number;
  times?: number[];
  max_energy_error: number;
  initial_energy: number;
  final_energy: number;
  angular_momentum_initial?: [number, number, number];
  angular_momentum_final?: [number, number, number];
  bodies: SimulationBodyState[];
  pairwise_distances?: SimulationPairwiseDistance[];
  energy_drift_series: {
    time: number;
    energy: number;
    kinetic?: number;
    potential?: number;
    energy_error: number;
  }[];
  reproducibility?: {
    scenario_id: string;
    scenario_name: string;
    timestamp: string;
    software_version: Record<string, string>;
    parameters: Record<string, any>;
    initial_conditions: any[];
    assumptions: string[];
    units: Record<string, string>;
    scientific_disclaimer: string;
  };
}


export interface HohmannTransferResult {
  origin_name: string;
  target_name: string;
  origin_radius_au: number;
  target_radius_au: number;
  transfer_semi_major_axis_au: number;
  transfer_eccentricity: number;
  delta_v1_km_s: number;
  delta_v2_km_s: number;
  total_delta_v_km_s: number;
  transfer_time_days: number;
  scientific_formulation: Record<string, string>;
}

export interface AIChatResponse {
  response: string;
  mode: UserMode;
  provider: string;
  used_fallback: boolean;
  is_grounded?: boolean;
  tools_invoked?: string[];
  distinctions?: {
    nebula_data?: string;
    computed_result?: string;
    external_scientific_context?: string;
    general_explanation?: string;
  };
  validation?: {
    is_valid: boolean;
    score: number;
    safety_flags: string[];
  };
  grounding_meta?: any;
}

export interface PersonaMetrics {
  word_count: number;
  sentence_count: number;
  flesch_reading_ease: number;
  flesch_kincaid_grade: number;
  technical_term_count: number;
  technical_term_density_percent: number;
  math_expressions_count: number;
  avg_words_per_sentence: number;
  grounding_score_percent: number;
  matched_points: number;
  total_points: number;
  latency_ms: number;
  response_sample: string;
}

export interface ResearchEvaluationResult {
  evaluation_id: string;
  query: string;
  target_object_id?: string | null;
  grounding_summary: any;
  researcher: PersonaMetrics;
  student: PersonaMetrics;
  citizen: PersonaMetrics;
  comparative_insights: {
    grade_level_contrast: string;
    technical_density_contrast: string;
    reading_ease_contrast: string;
    math_density_contrast: string;
  };
}

export interface EvaluationTask {
  id: string;
  task_number: number;
  name: string;
  category: string;
  route_target: string;
  target_object_id?: string;
  target_object_ids?: string[];
  scenario_id?: string;
  instruction: string;
  success_criteria: string;
  expected_value: string;
  grounding_field?: string;
  last_run?: {
    status: string;
    success: boolean;
    duration_ms: number;
    completed_at?: string;
    verification_details?: any;
  } | null;
}

export interface TaskRunResult {
  run_id: string;
  task_id: string;
  task_name: string;
  category: string;
  success: boolean;
  duration_ms: number;
  started_at: string;
  completed_at: string;
  verification_details: Record<string, any>;
}

export interface ScientificValidationBenchmark {
  id: string;
  property_name: string;
  category: string;
  formula: string;
  computed_value: number;
  reference_value: number;
  reference_source: string;
  units: string;
  tolerance: number;
  absolute_error: number;
  relative_error_pct?: number | null;
  passed: boolean;
  methodology_notes: string;
}

export interface ScientificValidationSuiteReport {
  suite_name: string;
  total_benchmarks: number;
  passed_count: number;
  failed_count: number;
  all_passed: boolean;
  benchmarks: ScientificValidationBenchmark[];
  scientific_disclaimer: string;
}

export interface TelemetrySummary {
  summary_timestamp: string;
  total_telemetry_events: number;
  task_completion: {
    total_executed: number;
    successful_count: number;
    failed_count: number;
    success_rate_percent: number;
    avg_completion_time_ms: number;
    tasks_by_category: Record<string, {
      total: number;
      success_rate_pct: number;
      avg_duration_ms: number;
    }>;
  };
  object_discovery: {
    total_discovery_events: number;
    avg_discovery_time_ms: number;
  };
  comparison: {
    total_comparisons_completed: number;
    avg_comparison_duration_ms: number;
  };
  visualization: {
    total_visualization_interactions: number;
    actions_breakdown: Record<string, number>;
  };
  simulation: {
    total_simulations_executed: number;
    avg_simulation_runtime_ms: number;
    avg_max_energy_drift: number;
  };
  ai_interactions: {
    total_queries: number;
    avg_latency_ms: number;
    grounding_fidelity_percent: number;
  };
  system_performance: {
    avg_page_load_ms: number;
    total_errors: number;
    error_rate_percent: number;
  };
  event_distribution: Record<string, number>;
  privacy_compliance: {
    pii_collected: boolean;
    anonymization_standard: string;
    compliant_with: string;
  };
}

