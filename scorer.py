def judge(question, expects, answer, results) -> bool:
    """
    Criterion 1 check: did retrieval actually find the answer?

    `expects` is the word or short phrase we'd expect a correct answer to
    contain, written in questions.py before any results existed. A run
    passes when that phrase shows up in the text of at least one retrieved
    chunk in `results` -- which is exactly what criterion 1 in criteria.md
    asks: "the retrieved chunks include one that contains the answer."

    This checks `results` (the chunks), not `answer` (the generated text),
    on purpose. Checking the answer instead would conflate two different
    failure modes into one number: retrieval missing the fact, and
    generation mangling or dropping a fact that WAS retrieved. Milestone 3
    asks you to tell those apart by printing the chunks and checking
    whether the answer is in there or not -- so the scorer needs to isolate
    the retrieval half on its own rather than deciding both at once.
    """
    expects_norm = expects.lower().strip()
    if not expects_norm:
        return None

    return any(expects_norm in r.text.lower() for r in results)