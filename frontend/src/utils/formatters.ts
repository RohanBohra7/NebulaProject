/**
 * Astronomical unit formatting utilities
 */

export function formatDistanceAU(au: number | null | undefined): string {
  if (au === null || au === undefined) return 'N/A';
  if (au < 0.001) return `${(au * 149597870.7).toLocaleString(undefined, { maximumFractionDigits: 1 })} km`;
  if (au < 10) return `${au.toFixed(3)} AU`;
  return `${au.toFixed(2)} AU`;
}

export function formatMassKg(kg: number | null | undefined): string {
  if (!kg) return 'N/A';
  const exponent = Math.floor(Math.log10(kg));
  const mantissa = kg / Math.pow(10, exponent);
  return `${mantissa.toFixed(3)} × 10^${exponent} kg`;
}

export function formatRadiusKm(km: number | null | undefined): string {
  if (!km) return 'N/A';
  return `${km.toLocaleString(undefined, { maximumFractionDigits: 1 })} km`;
}

export function formatPeriodDays(days: number | null | undefined): string {
  if (!days) return 'N/A';
  if (days < 1) return `${(days * 24).toFixed(1)} hours`;
  if (days > 365.25 * 2) return `${(days / 365.25).toFixed(2)} Earth years`;
  return `${days.toFixed(1)} days`;
}

export function formatTemperatureK(k: number | null | undefined): string {
  if (k === null || k === undefined) return 'N/A';
  const c = Math.round(k - 273.15);
  return `${k} K (${c > 0 ? `+${c}` : c}°C)`;
}

export function formatGravityMs2(g: number | null | undefined): string {
  if (g === null || g === undefined) return 'N/A';
  const earthG = (g / 9.807).toFixed(2);
  return `${g.toFixed(2)} m/s² (${earthG}g)`;
}
