function generateContent() {
  const text = getSelectedText().join('\n');
  return {
    text: text,
    content: generateFromText(text)
  };
}

function generateFromText(text) {
  const input = {
    input: text
  }

  const res = UrlFetchApp.fetch(
    `${getApiEndpoint()}/rag`,
    {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(input)
    }
  )

  const resJSON = JSON.parse(res.getContentText())

  let resultText = resJSON.output + "\n\n"
  resJSON.references.forEach(ref => resultText += `${ref.url}\n`)

  return resultText
}

function generateSimilarProblemContent() {
  const text = getSelectedText().join('\n');

  const input = {
    input: text,
    use_concepts: true
  }

  const res = UrlFetchApp.fetch(
    `${getApiEndpoint()}/similar-problem`,
    {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(input)
    }
  )

  const resJSON = JSON.parse(res.getContentText())

  let resultText = resJSON.similar_problem + "\n\n"
  resultText += `Inferred math concepts:\n${resJSON.concepts}\n\n`
  resultText += `Solution with work:\n${resJSON.solution_work}\n\n`


  return {
    text: text,
    content: resultText
  };
}

function generateWordProblemContent() {
  const text = getSelectedText().join('\n')

  const input = {
    input: text
  }

  const res = UrlFetchApp.fetch(
    `${getApiEndpoint()}/word-problem`,
    {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(input)
    }
  )

  const resJSON = JSON.parse(res.getContentText())

  let equation = "Equation: " + resJSON.equation + "\n\n"
  let scenario = "Scenario: " + resJSON.scenario + "\n\n"
  let question = "Question: " + resJSON.question + "\n\n"
  let answer = "Answer: " + resJSON.answer + "\n\n"
  let work = "Work: " + resJSON.work + "\n\n"
  let resultText = equation + scenario + question + answer + work

  return {
    text: text,
    content: resultText
  }

}
