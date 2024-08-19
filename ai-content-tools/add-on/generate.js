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

function generateContentWordProblemContent(problem_type) {
  const text = getSelectedText().join('\n');

  const input = {
    input: text,
    problem_type: problem_type
  }

  const res = UrlFetchApp.fetch(
    `${getApiEndpoint()}/content-word-problem`,
    {
      method: 'POST',
      contentType: 'application/json',
      payload: JSON.stringify(input)
    }
  )

  const resJSON = JSON.parse(res.getContentText())

  let resultText = resJSON.content_word_problem + "\n\n"
  resultText += `Solution:\n${resJSON.solution_work}\n\n`


  return {
    text: text,
    content: resultText
  };
}
