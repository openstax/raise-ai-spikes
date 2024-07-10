import { ResponseList, ResourceList, Resource  } from '../../components/ResponseList'
import { TextInputForm } from '../../components/TextInputForm'
import { BookSelection, Book } from '../../components/BookSelection'
export { Page }
import styled from 'styled-components'
import { useState } from 'react'
import { ENV } from '../../utils/env'

const CenteredContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  background-color: #ebebeb;
  min-height: 100vh; `

function Page() {
  const [responses, setResponses] = useState<ResourceList>({ responses: [] })
  const [subject, setSubject] = useState('')
  const [error, setError] = useState('')

  const books: Book[] = [{
    friendlyName: 'Algebra',
    subject: 'algebra'
  }, {
    friendlyName: 'History',
    subject: 'history'
  }
  ]
  const handleSubmit = async (input: string): Promise<void> => {
    setResponses({ responses: [] })
    setError('')

    try {
      const searchResults: Resource[] = await callMatchApi(input)

      if (searchResults.length === 0) {
        setError('No resources found')
      }

      setResponses({ responses: searchResults })
    } catch (error) {
      setError(String(error))
      setResponses({ responses: [] })
    }
  }

  const callMatchApi = async (input: string): Promise<Resource[]> => {
    try {
      const response = await fetch(`${ENV.RESOURCEMATCH_API}/match`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          model: 'gpt-3.5-turbo-1106',
          subject: subject,
          text: input
        })
      })

      if (!response.ok) {
        throw new Error('Request failed')
      }

      const data = await response.json()
      return data
    } catch (error) {
      throw new Error('Request failed')
    }
  }

  const onSelectBook = (subject: string) => {
    setSubject(subject)
  }
  return (
    <CenteredContainer>
      <h1>OpenStax AI Search</h1>
      <BookSelection books={books} onSelectBook={onSelectBook} />
      <TextInputForm onSubmit={handleSubmit} subject={subject} />
      {error.length !== 0? <h2>{error}</h2>: <></>}
      {responses.responses.length !== 0 ? <ResponseList resources={responses} /> : <></>}
    </CenteredContainer>
  )
}
