export function formatRelativeTime(seconds) {
  if (seconds <= 0) return "TIME UP!";
  const days = Math.floor(seconds / 86400);
  const hours = Math.floor((seconds % 86400) / 3600);
  const mins = Math.floor((seconds % 3600) / 60);
  const secs = seconds % 60;

  if (days > 0) {
    return `${days}D ${hours}H ${mins}M`;
  }
  return `${hours.toString().padStart(2, "0")}:${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
}

export function getCategoryBadgeColor(category = "") {
  const cat = category.toLowerCase();
  switch (cat) {
    case "drainage":
      return "bg-sky-100 text-blue-700 border-blue-600";
    case "pothole":
    case "road_damage":
      return "bg-amber-100 text-amber-800 border-amber-600";
    case "garbage":
    case "illegal_dumping":
      return "bg-emerald-100 text-emerald-800 border-emerald-600";
    case "broken_streetlight":
      return "bg-yellow-100 text-yellow-800 border-yellow-600";
    case "water_leakage":
      return "bg-cyan-100 text-cyan-800 border-cyan-600";
    default:
      return "bg-purple-100 text-purple-800 border-purple-600";
  }
}
