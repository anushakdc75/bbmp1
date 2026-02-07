export default function Admin() {
  return (
    <div className="grid grid-cols-3 gap-4 h-full content-start">
      <div className="panel p-4">Queue Filters<br/>Area / Category / Severity</div>
      <div className="panel p-4">Authority Assignment<br/>Level-2 Routing</div>
      <div className="panel p-4">SLA Operations<br/>Reminders / Escalations</div>
    </div>
  )
}
