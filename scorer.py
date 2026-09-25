def judge(question: str, expects: str, answer: str, results) -> bool:
    '''Evaluate whether the system's generated answer contains the expected text'''
    if not expects:
        return False
    return expects.strip().lower() in (answer or "").lower()

def retrieval_hit(expects: str, results) -> bool:
    '''Checks if any of the retrieved document chunks contain the expected text'''
    if not expects:
        return False
    target = expects.strip().lower()
    return any(target in (r.text or "").lower() for r in results)

def chunk_detailed(results, min_length: int = 250) -> bool:
    '''Checks if any retrieved chunk is at least min_length characters long'''
    return any(len(r.text or "") >= min_length for r in results)