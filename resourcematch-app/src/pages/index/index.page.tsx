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
  const [slug, setSlug] = useState('')
  const [error, setError] = useState('')

  const books: Book[] = [{
    friendlyName: 'Algebra',
    slug: 'college-algebra-corequisite-support-2e'
  }, {
    friendlyName: 'History',
    slug: 'world-history-volume-2'
  }
  ]
  const handleSubmit = async (input: string): Promise<void> => {
    setResponses([])
    const urls: string[] = await callMatchApi(input)
    if(urls.length === 0){
      setError('No resources found')
    }else{
      setError('')
    }
    setResponses(urls)
  }

  const callMatchApi = async (input: string) => {

    const response = await fetch(`${ENV.RESOURCEMATCH_API}/match`,  {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        model: 'gpt-3.5-turbo-1106',
        books: [slug],
        text: input
      })
    })

    if (!response.ok) {
      setError('Request failed')
      throw new Error('Request failed')
    }

    const data = await response.json()
    return data.urls
  }

  const onSelectBook = (slug: string) => {
    setSlug(slug)
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
