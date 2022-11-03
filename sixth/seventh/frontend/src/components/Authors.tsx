import React, { useState, useEffect } from "react";
import { gql, GraphQLClient } from "graphql-request";
import Books, { Book } from "./Books";

type authorProps = {
  client: GraphQLClient;
};

type author = {
  id: number;
  name: string;
  books: Book[];
};

export const authorExists = async (client: GraphQLClient, name: string) => {
  const query = gql`
        {
            authorByName(name: "${name}") {
                id
            }
        }
    `;

  const data = await client.request(query);
  return data["authorByName"];
};

export default function Authors({ client }: authorProps) {
  const [authors, setAuthors] = useState<author[]>([]);
  const authorsQuery = gql`
    {
      authors {
        id
        name
        books {
          name
        }
      }
    }
  `;
  useEffect(() => {
    client.request(authorsQuery).then(data => setAuthors(data["authors"]));
  }, []);

  return (
    <div className="Authors">
      <h2>Authors</h2>
      {authors.map(author => (
        <div key={author.id}>
          <h4>
            {author.id}. {author.name}
          </h4>
          <Books books={author.books} />
        </div>
      ))}
    </div>
  );
}
