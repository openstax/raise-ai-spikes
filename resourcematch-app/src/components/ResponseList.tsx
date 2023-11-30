import styled from 'styled-components'

interface ResponseListProps {
  responses: string[]
}

const StyledResponseList = styled.div`
  align-items: center;
  padding: 10px;
`

const StyledListItem = styled.li`
  list-style: none;
  border-bottom: 1px solid #eee;
  padding: 8px 0;
  cursor: pointer;

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
`

const CenteredHeading = styled.h2`
  text-align: center;
`

const StyledList = styled.ul`
  max-height: 500px;
  overflow-y: auto; 
  padding: 0;
`



export function ResponseList({ responses }: ResponseListProps): JSX.Element {
  return (
    <StyledResponseList>
      <CenteredHeading>Resources found</CenteredHeading>
      <StyledList>
        {responses.map((response, index) => (
          <StyledListItem key={index}>
            <a href={response} target="_blank" rel="noreferrer" >
              {response}
            </a>
          </StyledListItem>
        ))}
      </StyledList>
    </StyledResponseList>
  )
}
