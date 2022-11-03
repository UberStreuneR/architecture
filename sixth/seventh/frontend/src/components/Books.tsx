import React from "react";

export type Book = {
  id: number;
  name: string;
  authorId: number;
};

type bookProps = {
  books: Book[];
};

export default function Books({ books }: bookProps) {
  return (
    <div>
      {books.map(book => (
        <p key={book.id}>{book.name}</p>
      ))}
    </div>
  );
}
