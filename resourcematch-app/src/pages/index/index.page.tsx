import { ResponseList } from '../../components/ResponseList'
import { TextInputForm } from '../../components/TextInputForm'
import { BookSelection, Book } from '../../components/BookSelection'
export { Page }
import styled from 'styled-components'
import { useState } from 'react'
import { ENV } from '../../utils/env'

const CenteredContainer = styled.div`
  display: flex;
  width:100%;
  flex-direction: column;
  align-items: center;
`

function Page() {
  const [responses, setResponses] = useState<string[]>([]);
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
    setResponses([])
    setError('')

    try {
      const urls: string[] = await callMatchApi(input)

      if (urls.length === 0) {
        setError('No resources found')
      }

      setResponses(urls)
    } catch (error) {
      setError(String(error))
      setResponses([])
    }
  }

  const callMatchApi = async (input: string): Promise<string[]> => {
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
      return data.urls
    } catch (error) {
      throw new Error('Request failed')
    }
  }

  const onSelectBook = (subject: string) => {
    setSubject(subject)
  }
  return (
    <CenteredContainer>
      <h1>Resourcematch</h1>
      <BookSelection books={books} onSelectBook={onSelectBook} />
      <TextInputForm onSubmit={handleSubmit} />
      {error.length !== 0? <h2>{error}</h2>: <></>}
      {responses.length !== 0 ? <ResponseList responses={responses} /> : <></>}
    </CenteredContainer>
  )
}
