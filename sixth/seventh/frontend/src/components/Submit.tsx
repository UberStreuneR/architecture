import { gql, GraphQLClient } from "graphql-request";
import React, { useState } from "react";
import { authorExists } from "./Authors";

type submitProps = {
  client: GraphQLClient;
};

export default function Submit({ client }: submitProps) {
  const [name, setName] = useState("");
  const [author, setAuthor] = useState("");

  const bookMutation = gql`
    mutation addBook($name: String!, $authorId: Int!) {
      addBook(name: $name, authorId: $authorId) {
        id
      }
    }
  `;
  const authorMutation = gql`
    mutation addAuthor($name: String!) {
      addAuthor(name: $name) {
        id
      }
    }
  `;

  const handleSubmit = async () => {
    if (name && author) {
      let data = await authorExists(client, author);
      let authorId;
      if (data) {
        authorId = data.id;
        await client.request(bookMutation, { name: name, authorId: authorId });
      } else {
        let result = await client.request(authorMutation, { name: author });
        await client.request(bookMutation, {
          name: name,
          authorId: result.addAuthor.id,
        });
      }
    }
  };

  return (
    <div>
      <h2>Submit a book</h2>
      <p>
        <label htmlFor="bookAuthor" style={{ marginRight: "0.5rem" }}>
          Book Author
        </label>
        <input
          type="text"
          name=""
          id="bookAuthor"
          onChange={e => setAuthor(e.target.value)}
        />
      </p>
      <p>
        <label htmlFor="bookName" style={{ marginRight: "0.5rem" }}>
          Book Name
        </label>
        <input
          type="text"
          name=""
          id="bookName"
          onChange={e => setName(e.target.value)}
        />
      </p>
      <button onClick={handleSubmit}>Submit</button>
    </div>
  );
}
