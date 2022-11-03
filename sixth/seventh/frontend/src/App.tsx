import "./App.css";
import { GraphQLClient } from "graphql-request";
import { GRAPHQL_ENDPOINT } from "./data/constants";
import Authors from "./components/Authors";
import Submit from "./components/Submit";

function App() {
  const client = new GraphQLClient(GRAPHQL_ENDPOINT);

  return (
    <div>
      <h1>Library</h1>
      <div className="Library">
        <Authors client={client} />
        <Submit client={client} />
      </div>
    </div>
  );
}

export default App;
