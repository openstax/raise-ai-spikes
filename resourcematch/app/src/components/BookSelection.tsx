import React, { useState } from 'react'
import styled from 'styled-components'

export interface Book {
  friendlyName: string
  subject: string
}

const StyledBookSelectionWrapper = styled.div`
  padding: 20px; 
`

const StyledSelect = styled.select`
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  margin-top: 5px;
  justify-content: center;

`


interface BookSelectionProps {
  books: Book[]
  onSelectBook: (slug: string) => void
}

export function BookSelection({ books, onSelectBook }: BookSelectionProps): JSX.Element {
  const [selectedBook, setSelectedBook] = useState<string>('')

  const handleBookChange = (event: React.ChangeEvent<HTMLSelectElement>): void => {
    const selectedSlug = event.target.value
    setSelectedBook(selectedSlug)
    onSelectBook(selectedSlug)
  }

  return (
    <StyledBookSelectionWrapper>
      <StyledSelect value={selectedBook} onChange={handleBookChange}>
        <option value="">Select a subject</option>
        {books.map((book) => (
          <option key={book.subject} value={book.subject}>
            {book.friendlyName}
          </option>
        ))}
      </StyledSelect>
    </StyledBookSelectionWrapper>
  )
}
