return function View() {
  const [hoveredGroup, setHoveredGroup] = dc.useState(null);
  const singleHourRegex = /^(\d{2}:\d{2})/;
  const doubleHourRegex = /^(\d{2}:\d{2}) - (\d{2}:\d{2})/;
  const listes = dc
    .useQuery('@list-item and path("6 Journal")')
    .filter(
      (l) => singleHourRegex.test(l.$text) || doubleHourRegex.test(l.$text)
    );
  listes.sort((a, b) => {
    const dateAMatch = a.$file
      .split("/")
      .slice(-1)[0]
      .match(/\d{2}-\d{2}-\d{4}/);
    const dateBMatch = b.$file
      .split("/")
      .slice(-1)[0]
      .match(/\d{2}-\d{2}-\d{4}/);
    const dateA = new Date(dateAMatch[0].split("-").reverse().join("-"));
    const dateB = new Date(dateBMatch[0].split("-").reverse().join("-"));
    return dateA - dateB;
  });
  const groupes = {
    Obsidian: "#obsidian",
    "Recherche d'emploi": "Candidatures",
    Lecture: "livre",
  };
  const getFormattedDate = (filepath) => {
    const match = filepath
      .split("/")
      .slice(-1)[0]
      .match(/\d{2}-\d{2}-\d{4}/);
    return match ? match[0] : "Date inconnue";
  };
  const timeToMinutes = (time) =>
    time
      .split(":")
      .map(Number)
      .reduce((a, b) => a * 60 + b);
  const calculateDuration = (start, end) =>
    timeToMinutes(end) +
    (timeToMinutes(end) < timeToMinutes(start) ? 24 * 60 : 0) -
    timeToMinutes(start);
  const timeSpentByDayAndGroup = {};
  const totalTimeByGroup = {};
  const timeSpentByWeek = {};
  listes.forEach((tache, index) => {
    const dateStr = getFormattedDate(tache.$file);
    const dateParts = dateStr.split("-");
    const date = new Date(dateParts[2], dateParts[1] - 1, dateParts[0]);
    let [startTime, endTime] =
      (tache.$text.match(doubleHourRegex) ||
        tache.$text.match(singleHourRegex))?.[0]?.split(" - ") || [];
    if (startTime && !endTime) {
      const nextTask = listes[index + 1];
      if (nextTask && nextTask.$file === tache.$file) {
        const nextTaskTime =
          nextTask.$text.match(doubleHourRegex) ||
          nextTask.$text.match(singleHourRegex);
        if (nextTaskTime) {
          endTime = nextTaskTime[0].split(" - ")[1] || nextTaskTime[0];
        }
      }
    }
    if (startTime && endTime) {
      const duration = calculateDuration(startTime, endTime);
      for (let group in groupes) {
        if (tache.$text.includes(groupes[group])) {
          if (!timeSpentByDayAndGroup[dateStr])
            timeSpentByDayAndGroup[dateStr] = {};
          if (!timeSpentByDayAndGroup[dateStr][group])
            timeSpentByDayAndGroup[dateStr][group] = 0;
          timeSpentByDayAndGroup[dateStr][group] += duration;
          if (!totalTimeByGroup[group]) totalTimeByGroup[group] = 0;
          totalTimeByGroup[group] += duration;
          const weekStart = new Date(date);
          weekStart.setDate(weekStart.getDate() - weekStart.getDay() + 1);
          const weekKey = weekStart.toISOString().split("T")[0];
          if (!timeSpentByWeek[weekKey]) timeSpentByWeek[weekKey] = {};
          if (!timeSpentByWeek[weekKey][group])
            timeSpentByWeek[weekKey][group] = 0;
          timeSpentByWeek[weekKey][group] += duration;
        }
      }
    }
  });
  const lastFiveWeeks = Object.keys(timeSpentByWeek).slice(-5).reverse();
  const formatDate = (date) =>
    new Date(date).toLocaleDateString("fr-FR", {
      day: "numeric",
      month: "long",
    });
  const totalTime = Object.values(totalTimeByGroup).reduce((a, b) => a + b, 0);
  const percentages = Object.keys(totalTimeByGroup).map((group) => {
    const percentage = (totalTimeByGroup[group] / totalTime) * 100;
    return { group, percentage: Math.round(percentage) };
  });
  const generateCSV = async () => {
    let csvContent = "Nom, Heure de début, Heure de fin, Durée, Date, Groupe\n";
    listes.forEach((tache, index) => {
      let [startTime, endTime] =
        (tache.$text.match(doubleHourRegex) ||
          tache.$text.match(singleHourRegex))?.[0]?.split(" - ") || [];
      const dateStr = getFormattedDate(tache.$file);
      if (startTime && !endTime) {
        const nextTask = listes[index + 1];
        if (nextTask && nextTask.$file === tache.$file) {
          endTime = nextTask.$text.match(singleHourRegex)?.[0];
        }
      }
      let taskDescription = tache.$text
        .replace(doubleHourRegex, "")
        .replace(singleHourRegex, "")
        .trim();
      if (startTime && endTime) {
        const duration = calculateDuration(startTime, endTime);
        for (let group in groupes) {
          if (tache.$text.includes(groupes[group])) {
            csvContent += `${taskDescription}; ${startTime}; ${endTime}; ${duration}; ${dateStr}; ${group}\n`;
          }
        }
      }
    });
    let file = await app.vault.getAbstractFileByPath(
      "bins/export_tracker_obsidian.csv"
    );
    await app.vault.modifyBinary(file, csvContent);
  };
  return (
    <div>
      {" "}
      <h2>Total temps par groupe</h2>{" "}
      <ul>
        {Object.keys(totalTimeByGroup).map((group) => (
          <li key={group}>
            {group} : {Math.floor(totalTimeByGroup[group] / 60)}h{" "}
            {totalTimeByGroup[group] % 60}min
          </li>
        ))}
      </ul>{" "}
      <h2>Temps moyen par groupe par semaine</h2>{" "}
      <ul>
        {Object.keys(totalTimeByGroup).map((group) => {
          const average = Math.round(
            totalTimeByGroup[group] / lastFiveWeeks.length
          );
          return (
            <li key={group}>
              {group} : {Math.floor(average / 60)}h {average % 60}min / semaine
            </li>
          );
        })}
      </ul>{" "}
      <h2>Graphique en camembert des temps par groupe</h2>{" "}
      <div
        style={{ display: "flex", flexDirection: "row", alignItems: "center" }}
      >
        {" "}
        <svg width="200" height="200" xmlns="http://www.w3.org/2000/svg">
          {" "}
          <circle
            cx="100"
            cy="100"
            r="80"
            fill="none"
            stroke="#ddd"
            strokeWidth="0"
          />{" "}
          {(() => {
            const colors = {
              Obsidian: "#7765ac",
              "Recherche d'emploi": "#FFC300",
              Lecture: "#3498DB",
            };
            let totalTime = Object.values(totalTimeByGroup).reduce(
              (a, b) => a + b,
              0
            );
            let currentAngle = 0;
            return Object.keys(totalTimeByGroup).map((group) => {
              const time = totalTimeByGroup[group];
              const angle = (time / totalTime) * 2 * Math.PI;
              const x1 = 100 + 80 * Math.cos(currentAngle);
              const y1 = 100 + 80 * Math.sin(currentAngle);
              currentAngle += angle;
              const x2 = 100 + 80 * Math.cos(currentAngle);
              const y2 = 100 + 80 * Math.sin(currentAngle);
              const largeArcFlag = angle > Math.PI ? 1 : 0;
              const d = `M100,100 L${x1},${y1} A80,80 0 ${largeArcFlag} 1 ${x2},${y2} Z`;
              const fillColor =
                hoveredGroup === group ? "#656565" : colors[group];
              return (
                <path
                  data-legende={group}
                  className="getClass"
                  d={d}
                  fill={fillColor}
                  style={{ transition: "transform 0.3s", cursor: "pointer" }}
                  onMouseOver={() => setHoveredGroup(group)}
                  onMouseOut={() => setHoveredGroup(null)}
                />
              );
            });
          })()}{" "}
        </svg>{" "}
        <ul>
          {" "}
          {Object.keys(totalTimeByGroup).map((group) => {
            const time = totalTimeByGroup[group];
            console.log(time)
            console.log(totalTime)
            const percentage = ((time / totalTime) * 100).toFixed(1);
            return (
              <li key={group}>
                {" "}
                <span id={group + "_color"}></span>{" "}
                <strong
                  style={{
                    fontWeight: hoveredGroup === group ? "bold" : "normal",
                  }}
                >
                  {group} : {percentage}%
                </strong>{" "}
              </li>
            );
          })}{" "}
        </ul>{" "}
      </div>{" "}
      <h2>Temps par semaine</h2>{" "}
      {lastFiveWeeks.map((week) => {
        const weekStart = new Date(week);
        const weekEnd = new Date(weekStart);
        weekEnd.setDate(weekStart.getDate() + 6);
        return (
          <div key={week}>
            {" "}
            <h3>
              Du {formatDate(weekStart)} au {formatDate(weekEnd)}
            </h3>{" "}
            <ul>
              {Object.keys(timeSpentByWeek[week]).map((group) => (
                <li key={group}>
                  {group} : {Math.floor(timeSpentByWeek[week][group] / 60)}h{" "}
                  {timeSpentByWeek[week][group] % 60}min
                </li>
              ))}
            </ul>{" "}
          </div>
        );
      })}{" "}
      <button onClick={generateCSV}>Générer CSV</button> <h2>Temps par jour</h2>{" "}
      {Object.keys(timeSpentByDayAndGroup)
        .sort((a, b) => {
          const dateA = new Date(a.split("-").reverse().join("-"));
          const dateB = new Date(b.split("-").reverse().join("-"));
          return dateB - dateA;
        })
        .map((date) => (
          <div key={date}>
            {" "}
            <h3>{date}</h3>{" "}
            <ul>
              {" "}
              {Object.keys(timeSpentByDayAndGroup[date]).map((group) => (
                <li key={group}>
                  {" "}
                  {group} :{" "}
                  {Math.floor(timeSpentByDayAndGroup[date][group] / 60)}h{" "}
                  {timeSpentByDayAndGroup[date][group] % 60}min{" "}
                </li>
              ))}{" "}
            </ul>{" "}
          </div>
        ))}{" "}
    </div>
  );
};
