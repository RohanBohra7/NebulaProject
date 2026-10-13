import { logTelemetryEvent } from './api';

/**
 * Lightweight client-side telemetry service for NEBULA.
 * Collects non-sensitive performance, interaction, and usability metrics.
 * Strictly zero personally identifiable information (PII).
 */

export function trackPageView(pageName: string, durationMs?: number) {
  logTelemetryEvent({
    event_type: 'page_load',
    component: pageName,
    duration_ms: durationMs,
    success: true,
    metadata: { route: window.location.pathname }
  });
}

export function trackVisualizationInteraction(action: string, targetBody?: string, fps?: number) {
  logTelemetryEvent({
    event_type: 'visualization_interaction',
    component: '3d_visualizer',
    success: true,
    metadata: { action, targetBody, fps }
  });
}

export function trackObjectDiscovery(searchTerm: string, objectId?: string, discoveryTimeMs?: number) {
  logTelemetryEvent({
    event_type: 'object_discovery',
    component: 'explorer',
    duration_ms: discoveryTimeMs,
    success: true,
    metadata: { searchTerm, objectId }
  });
}

export function trackComparisonCompletion(objectIds: string[], durationMs?: number, mode?: string) {
  logTelemetryEvent({
    event_type: 'comparison_completion',
    component: 'comparison',
    duration_ms: durationMs,
    success: true,
    metadata: { objectIds, count: objectIds.length, mode }
  });
}

export function trackSimulationRun(scenarioId: string, durationMs?: number, steps?: number, maxEnergyError?: number) {
  logTelemetryEvent({
    event_type: 'simulation_completion',
    component: 'simulation',
    duration_ms: durationMs,
    success: true,
    metadata: { scenarioId, steps, maxEnergyError }
  });
}

export function trackAIInteraction(mode: string, latencyMs: number, toolsInvoked: number, isGrounded: boolean) {
  logTelemetryEvent({
    event_type: 'ai_interaction',
    component: 'ai_assistant',
    duration_ms: latencyMs,
    success: true,
    metadata: { mode, toolsInvoked, isGrounded }
  });
}

export function trackSystemError(component: string, errorMessage: string) {
  logTelemetryEvent({
    event_type: 'system_error',
    component,
    success: false,
    metadata: { errorMessage: errorMessage.slice(0, 150) }
  });
}
