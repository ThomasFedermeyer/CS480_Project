import React, { useEffect, useState } from "react";

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetch(
      "http://127.0.0.1:8000/popular_technologies/getUsersAndDeveloperTypesPerTechnology?developerTypeName=Full-Stack Engineer"
    )
      .then((response) => response.json())
      .then((data) => setData(data))
      .catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : "Loading..."}
    </div>
  );
}

export default App;
