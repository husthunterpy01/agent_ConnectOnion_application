import { useCallback, useMemo, useState } from "react";
import "./App.css";

const diffInDays = (dateString) => {
  const target = new Date(dateString);
  const today = new Date();
  target.setHours(0, 0, 0, 0);
  today.setHours(0, 0, 0, 0);
  return Math.round((target - today) / (1000 * 60 * 60 * 24));
};

const formatDate = (dateString) =>
  new Date(dateString).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
    year: "numeric",
  });

function App() {
  const [report, setReport] = useState(null);
  const [error, setError] = useState("");
  const [lastUpdated, setLastUpdated] = useState(null);

  const handleFileUpload = async (event) => {
    setError("");
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      const text = await file.text();
      const json = JSON.parse(text);
      setReport(json);
      setLastUpdated(new Date());
    } catch (err) {
      console.error(err);
      setError("Invalid JSON file. Please export the latest report and try again.");
    }
  };

  const loadSample = useCallback(async () => {
    try {
      const response = await fetch("/sample-report.json");
      const json = await response.json();
      setReport(json);
      setLastUpdated(new Date());
      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to load sample report.");
    }
  }, []);

  const notifications = useMemo(() => {
    if (!report?.tracker?.schedules) return [];
    const upcoming = [];
    report.tracker.schedules.forEach((schedule) => {
      schedule.milestones?.forEach((milestone) => {
        const days = diffInDays(milestone.due);
        if (days >= 0 && days <= 10) {
          upcoming.push({
            scholarshipId: schedule.scholarship_id,
            label: milestone.label,
            due: milestone.due,
            days,
          });
        }
      });
    });
    return upcoming.sort((a, b) => a.days - b.days);
  }, [report]);

  const scholarshipCards = useMemo(() => report?.ranker?.ranked ?? [], [report]);
  const universityCards = useMemo(
    () => report?.universities?.recommendations ?? [],
    [report],
  );

  return (
    <div className="app-shell">
      <header className="app-header">
        <div>
          <p className="eyebrow">ResearchScholar AI</p>
          <h1>Scholarship + University Radar</h1>
        </div>
        <div className="cta-row">
          <label className="upload-label">
            <input type="file" accept="application/json" onChange={handleFileUpload} />
            Upload report.json
          </label>
          <button type="button" onClick={loadSample}>
            Load sample data
          </button>
        </div>
      </header>

      {error && <div className="alert error">{error}</div>}
      {lastUpdated && (
        <div className="alert info">
          Latest data loaded {lastUpdated.toLocaleString()}
        </div>
      )}

      {!report && (
        <section className="placeholder">
          <h2>Bring your AI-generated report</h2>
          <p>
            Run <code>python agent.py --output report.json</code> in <code>my-agent/</code>,
            then drop the exported JSON here to visualize scholarships, universities, and
            upcoming deadlines. Or, use the sample data to explore the interface.
          </p>
        </section>
      )}

      {notifications.length > 0 && (
        <section className="notifications">
          <h2>Upcoming milestones</h2>
          <div className="notification-grid">
            {notifications.map((item) => (
              <article key={`${item.scholarshipId}-${item.label}`} className="notification-card">
                <p className="overline">{item.label}</p>
                <h3>{formatDate(item.due)}</h3>
                <p>
                  {item.days === 0
                    ? "Due today"
                    : item.days === 1
                      ? "Due tomorrow"
                      : `Due in ${item.days} days`}
                </p>
                <p className="muted">Scholarship: {item.scholarshipId}</p>
              </article>
            ))}
          </div>
        </section>
      )}

      {report && (
        <>
          <section className="profile-card">
            <div>
              <p className="eyebrow">Profile</p>
              <h2>{report.profile?.name ?? "Unknown"}</h2>
              <p>{report.profile?.goals}</p>
            </div>
            <dl>
              <div>
                <dt>Academic Level</dt>
                <dd>{report.profile?.academic_level}</dd>
              </div>
              <div>
                <dt>Major</dt>
                <dd>{report.profile?.major}</dd>
              </div>
              <div>
                <dt>Location</dt>
                <dd>{report.profile?.location}</dd>
              </div>
              <div>
                <dt>GPA</dt>
                <dd>{report.profile?.gpa}</dd>
              </div>
            </dl>
          </section>

          <section>
            <div className="section-heading">
              <div>
                <p className="eyebrow">Scholarships</p>
                <h2>Ranked opportunities</h2>
              </div>
              <span className="badge">{scholarshipCards.length} tracked</span>
            </div>
            <div className="card-grid">
              {scholarshipCards.map((entry) => (
                <article key={entry.scholarship.id} className="data-card">
                  <header>
                    <h3>{entry.scholarship.title}</h3>
                    <p>{entry.scholarship.sponsor}</p>
                  </header>
                  <p className="score">Score {entry.score}/100</p>
                  <p className="muted">{entry.reasoning}</p>
                  <p className="muted">Deadline: {formatDate(entry.scholarship.deadline)}</p>
                  <a href={entry.scholarship.url} target="_blank" rel="noreferrer">
                    View details →
                  </a>
                </article>
              ))}
            </div>
          </section>

          <section>
            <div className="section-heading">
              <div>
                <p className="eyebrow">University Matches</p>
                <h2>Programs aligned to your profile</h2>
              </div>
              <span className="badge">{universityCards.length} suggested</span>
            </div>
            <div className="card-grid">
              {universityCards.map((entry) => (
                <article key={entry.university.id} className="data-card">
                  <header>
                    <h3>{entry.university.name}</h3>
                    <p>{entry.university.location}</p>
                  </header>
                  <p className="score">Match score {entry.score}</p>
                  <ul>
                    {entry.fit_reasons?.map((reason) => (
                      <li key={reason}>{reason}</li>
                    ))}
                  </ul>
                  <p className="muted">Tuition support: {entry.university.tuition_support}</p>
                  <a href={entry.university.website} target="_blank" rel="noreferrer">
                    Visit program →
                  </a>
                </article>
              ))}
            </div>
          </section>
        </>
      )}
    </div>
  );
}

export default App;
