def process_file(fname):
    """Given a TeX file name, return a list of \items."""
    with open(fname, "r") as fp:
        contents = fp.read()

    # FIXME: this is brittle, and will produce bogus if e.g. \begin{enumerate}
    # is followed by a TeX comment: \begin{enumerate} % [resume]

    # extract the \enumerate, discard the rest
    try:
        items = contents.split("\\begin{enumerate}[resume]")[1]
    except IndexError:
        # no {enumerate}[resume]?
        items = contents.split("\\begin{enumerate}")[1]

    items = items.split("\\end{enumerate}")[0]

    # extract individual items, discard empty lines
    questions = [q for q in items.split("\\item") if q.strip()]
    return questions


def collect_questions(fnamelist):
    """Collect all questions from a list of files.

    Returns a dict of {course, list of questions}
    """
    mapping = {}
    for fname in fnamelist:
        if not fname.endswith(".tex"):
            fname = fname + ".tex"
        questions = process_file("./src/" + fname)
        mapping[fname[:-4]] = questions
    return mapping


def create_variants(scheme, mapping=None):
    """Create exam variants.

    Parameters:
    -----------
    scheme : a list of lists of 2-tuples
        Each list is a variant.
        Each 2-tuple is a pair of the course & the number of the question
        The course is a key to the `mapping` argument.
    mapping : dict, optional
        The keys are the course names, and the values are the lists of questions
        Is constructed from the scheme if not provided.

    Returns:
    --------
    A list of questions, spelled out in full, as specified by `questions`
    """
    if mapping is None:
        # collect the unique course names from the scheme
        fnames = set()
        for var in scheme:
            for pair in var:
                fnames.add(pair[0])

        # collect all questions for all courses, keyed by the course name
        mapping = collect_questions(fnames)

    # create variants according to the scheme
    lst = []
    for variant in scheme:
        this_variant = [mapping[course][number] for course, number in variant]
        lst.append(this_variant)
    return lst


def create_all_variants(scheme, mapping=None, outf="BILETY.tex"):
    """Create the TeX file with all variants, for printing"""
    # read in the template
    with open("src/variants.template.tex.in", "r") as ft:
        template = ft.read()

    preamble, body = template.split("\\begin{document}")
    body = body.split("\\end{document}")[0]

    # create the questions themselves
    variants = create_variants(scheme, mapping)

    # write out
    with open(outf, "w") as fb:
        fb.write(preamble)

        fb.write("\\begin{document}\n\n")

        for n, variant in enumerate(variants):
            bilet = body.replace("###", str(n+1))
            qs = "\n\n\\item ".join([""] + variant)
            bilet = bilet.replace("@@@ QUESTIONS HERE @@@", qs)
            fb.write(bilet)

        fb.write("\\end{document}")


if __name__ == "__main__":
    #print(process_file("src/teormeh.tex"))
    #print(collect_questions(["funkan", "difur.tex"]))

    #exit(-1)

    scheme = [[("funkan", 1), ("matan", 2)],
              [("funkan", 0), ("difur", 1)],
              [("umf", 1), ("funkan", 1)],
             ]

    create_all_variants(scheme)

    exit(-1)

#    lst1 = create_variants(scheme)
#    for j, variant in enumerate(lst1):
#        print("\n ---------", j+1)
#        for q in variant:
#            print(q)

