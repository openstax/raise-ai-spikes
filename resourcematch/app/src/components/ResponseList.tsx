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
  section_title: string
  subsection_title: string,
  visible_content: string
}

const StyledResponseList = styled.div`
  padding: 10px;
`

const StyledListItem = styled.li`
  display: flex;
  flex-direction: column;
  padding: 10px;
  border-bottom: 1px solid #ccc;
  max-width: 800px;
  margin-bottom: 1rem;
  margin-right: .5rem;
  background-color: #f7f6f6; 

  &:hover {
    background-color: #cac6c6;
  }

  a {
    color: #333;
    align-self: end;

    &:hover {
      color: #007bff;
    }
  }

  .book-title {
    font-size: 20px;
    color: blue;
    font-weight: bold;
  }

  .section-title {
    font-size: 18px;
    color: #666;
  }

  .subsection-title {
    font-size: 16px;
    color: #666;
  }

  .content-flex {
    display: flex;
    flex-direction: column;
  }

  .content-text-spacing {
    margin: .5rem 0
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
            <div className="content-flex">
              <div>
                <p className="book-title content-text-spacing">{response.book_title}</p>
              </div>
              <div>
                <p className="section-title content-text-spacing">{response.section_title}</p>
              </div>
              <div>
                <p className="subsection-title content-text-spacing">{response.subsection_title}</p>
              </div>
              <div>
                <p className="visible-content content-text-spacing">{response.visible_content}</p>
              </div>
              <a href={response.url} className="view-more" target="_blank" rel="noreferrer" >
                View More
              </a>
            </div>
          </StyledListItem>
        ))}
      </StyledList>
    </StyledResponseList>
  )
}
