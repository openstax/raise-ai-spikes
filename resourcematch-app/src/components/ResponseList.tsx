import styled from 'styled-components'

export interface ResourceList {
  responses: Resource[]
}

interface ResponseListProps {
  resources: ResourceList
}

export interface Resource {
  url: string
  book_title: string
  chapter_title: string
  page_title: string,
  visible_content: string
}

const StyledResponseList = styled.div`
  align-items: center;
  padding: 10px;
`

const StyledListItem = styled.li`
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-bottom: 1px solid #ccc;
  width: 800px; 

  &:hover {
    background-color: #f7f7f7;
  }

  a {
    text-decoration: none;
    color: #333;

    &:hover {
      color: #007bff;
    }
  }

  .book-title {
    font-size: 20px;
    color: blue;
    font-weight: bold;
  }

  .chapter-title {
    font-size: 18px;
    color: #666;
  }
  .page-title {
    font-size: 16px;
    color: #666;
    margin-top: auto;
  }

  .view-more {
    font-size: 14px;
    color: #333;
    cursor: pointer;
    margin-left: auto;
    color: blue;
  }
  .visible-content {
    font-size: 12px;
    color: black;
  }
`

const CenteredHeading = styled.h2`
  text-align: center;
`

const StyledList = styled.ul`
  max-height: 500px;
  overflow-y: auto; 
  padding: 0;
`



export function ResponseList( {resources}: ResponseListProps): JSX.Element {
  return (
    <StyledResponseList>
      <CenteredHeading>Here’s what we found</CenteredHeading>
      <StyledList>
        {resources.responses.map((response, index) => (
          <StyledListItem key={index}>
            <div className="book-title">{response.book_title}</div>
            <div className="chapter-title">{response.chapter_title}</div>
            <div className="page-title">{response.page_title}</div>
            <br/>
            <div className="visible-content">{response.visible_content}</div>
            <a href={response.url} className="view-more" target="_blank" rel="noreferrer" >
              View More
            </a>
          </StyledListItem>
        ))}
      </StyledList>
    </StyledResponseList>
  )
}
