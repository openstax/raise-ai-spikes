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
`;



export function ResponseList({ responses }: ResponseListProps): JSX.Element {
  return (
    <StyledResponseList>
      <CenteredHeading>Resources found</CenteredHeading>
      <ul>
        {responses.map((response, index) => (
          <StyledListItem key={index}>
            <a href={response} target="_blank" rel="noreferrer" >
              {response}
            </a>
          </StyledListItem>
        ))}
      </ul>
    </StyledResponseList>
  )
}
