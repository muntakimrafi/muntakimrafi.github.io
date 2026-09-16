#!/usr/bin/env python3
"""Build the static pages for muntakimrafi's site.

Every page shares a masthead, a footer and a <head>; duplicating those seven
times by hand is how navigation drifts. Content lives in this file as plain
data, the chrome is assembled once, and the generated HTML is committed so
GitHub Pages serves it with no build step.

    python3 tools/build.py        # run from the site root

"""

import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NAME = "Abdul Muntakim Rafi"
ROLE = "PhD Candidate, University of British Columbia"

NAV = [
    ("index.html", "Home"),
    ("research.html", "Research"),
    ("publications.html", "Publications"),
    ("talks.html", "Talks"),
    ("teaching.html", "Teaching"),
    ("service.html", "Service"),
    ("cv.html", "CV"),
]

EMAIL = "rafi11@student.ubc.ca"
SCHOLAR = "https://scholar.google.com/citations?user=fyNavPkAAAAJ&hl=en"
GITHUB = "https://github.com/muntakimrafi"
LINKEDIN = "https://www.linkedin.com/in/abdul-muntakim-rafi-205002154/"
RESEARCHGATE = "https://www.researchgate.net/profile/Abdul-Muntakim-Rafi/publications"
CV_PDF = "data/CV_updated.pdf"
FAILURE_PDF = "data/CV_of_Failure.pdf"

ICONS = {
    "scholar": '<path fill="currentColor" d="M12 3 1 9l11 6 9-4.91V17h2V9L12 3zM5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/>',
    "github": '<path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.11.79-.25.79-.56v-2c-3.2.7-3.88-1.54-3.88-1.54-.53-1.34-1.29-1.7-1.29-1.7-1.05-.72.08-.7.08-.7 1.16.08 1.77 1.19 1.77 1.19 1.03 1.77 2.71 1.26 3.37.96.1-.75.4-1.26.73-1.55-2.56-.29-5.25-1.28-5.25-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.47.11-3.05 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.8 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.58.23 2.76.12 3.05.74.81 1.18 1.84 1.18 3.1 0 4.43-2.69 5.4-5.26 5.69.41.36.78 1.06.78 2.14v3.17c0 .31.21.68.8.56A11.5 11.5 0 0 0 12 .5z"/>',
    "linkedin": '<path fill="currentColor" d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3V9zm7 0h3.8v1.64h.05c.53-1 1.83-2.06 3.76-2.06 4.02 0 4.76 2.65 4.76 6.09V21h-4v-5.5c0-1.31-.02-3-1.83-3-1.83 0-2.11 1.43-2.11 2.91V21h-4V9z"/>',
    "mail": '<path fill="none" stroke="currentColor" stroke-width="1.7" d="M3 6h18v12H3zM3 6l9 7 9-7"/>',
}

# The address is never rendered as text anywhere on the site; it is reachable
# only through the envelope icon in the masthead and the footer.
SOCIAL = [
    ("mail", "mailto:" + EMAIL, "Email"),
    ("scholar", SCHOLAR, "Google Scholar"),
    ("github", GITHUB, "GitHub"),
    ("linkedin", LINKEDIN, "LinkedIn"),
]


def external(href):
    """mailto: links must not carry target/rel; http ones should."""
    return '' if href.startswith("mailto:") else ' target="_blank" rel="noopener"'



def icon(key, cls):
    return ('<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>'
            % (cls, ICONS[key]))


def head(title, description):
    full = title if title == NAME else "%s &middot; %s" % (title, NAME)
    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full}</title>
<meta name="author" content="{name}">
<meta name="description" content="{desc}">
<meta property="og:title" content="{full}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<link rel="icon" href="favicon.ico" sizes="any">
<link rel="icon" type="image/png" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&family=Public+Sans:wght@300;400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="assets/css/styles.css">
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
""".format(full=full, name=NAME, desc=description)


def masthead(current):
    links = []
    for href, label in NAV:
        if href == current:
            links.append('      <a href="%s" aria-current="page" class="is-current">%s</a>' % (href, label))
        else:
            links.append('      <a href="%s">%s</a>' % (href, label))

    social = []
    for key, href, label in SOCIAL:
        social.append('        <a href="%s"%s aria-label="%s" title="%s">%s</a>'
                      % (href, external(href), label, label, icon(key, "masthead__icon")))

    return """
<header class="masthead">
  <div class="wrap masthead__inner">
    <a class="brand" href="index.html">
      <span class="brand__name">{name}</span>
    </a>
    <nav class="nav" id="primary-nav" aria-label="Primary">
{links}
    </nav>
    <div class="masthead__end">
      <div class="masthead__social">
{social}
      </div>
      <button class="theme-toggle" id="theme-toggle" type="button" aria-label="Switch colour theme"><svg class="theme-toggle__icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path fill="currentColor" d="M12 3a9 9 0 0 0 0 18z"/></svg><span class="theme-toggle__label">Theme</span></button>
      <button class="nav-toggle" id="nav-toggle" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu"><svg class="nav-toggle__bars" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M4 7h16M4 12h16M4 17h16"/></svg><svg class="nav-toggle__x" viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" d="M6 6l12 12M18 6L6 18"/></svg></button>
    </div>
  </div>
</header>
""".format(name=NAME, links="\n".join(links), social="\n".join(social))


def footer():
    links = "\n".join('      <a href="%s">%s</a>' % (h, l) for h, l in NAV)
    social = "\n".join(
        '        <a class="social__link" href="%s"%s>%s<span>%s</span></a>'
        % (href, external(href), icon(key, "social__icon"), label)
        for key, href, label in SOCIAL)
    return """
<footer class="footer">
  <div class="wrap footer__inner">
    <div>
      <p class="footer__name">{name}</p>
      <p>Vancouver, Canada</p>
      <div class="social">
{social}
        <a class="social__link" href="{rg}" target="_blank" rel="noopener"><span>ResearchGate</span></a>
      </div>
    </div>
    <nav class="footer__links" aria-label="Footer">
{links}
      <a href="{cv}">CV (PDF)</a>
    </nav>
  </div>
</footer>

<script src="assets/js/main.js"></script>
</body>
</html>
""".format(name=NAME, social=social, rg=RESEARCHGATE, links=links, cv=CV_PDF)


def write(slug, title, description, main):
    html = head(title, description) + masthead(slug) + "\n<main id=\"main\">\n" + main.strip() + "\n</main>\n" + footer()
    path = os.path.join(ROOT, slug)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(html)
    return path


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------

ME = "Abdul Muntakim Rafi"


def authors(text):
    """Bold my own name wherever it appears in an author list."""
    return text.replace(ME, "<strong>%s</strong>" % ME)


# (year, title, url or None, authors, venue, [(label, url), ...])
PREPRINTS = [
    ("2026",
     "gRely: Reliability estimation of variant effect predictions for genome-trained sequence-to-expression models",
     None,
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, G&ouml;k&ccedil;en Eraslan, Kipper Fletez-Brant<sup>&dagger;</sup>",
     "In preparation", []),
    ("2026",
     "Evaluation of active learning selection strategies and characterization of informative sequences for sequence-to-expression models",
     None,
     "Justin Qian<sup>*</sup>, Abdul Muntakim Rafi<sup>*&dagger;</sup>, Emmanuel Cazottes<sup>*</sup>, Carl de Boer<sup>&dagger;</sup>",
     "In preparation", []),
    ("2025",
     "Yorzoi: Predicting RNA-seq coverage from DNA sequence in yeast",
     "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract",
     "Timon Schneider, Abdul Muntakim Rafi, Cassandra Jensen, Daniella Liao, Yiren Zhao, Carl de Boer, Tom Ellis",
     "bioRxiv",
     [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract")]),
    ("2025",
     "Detecting and avoiding homology-based data leakage in genome-trained sequence models",
     "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v1.abstract",
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, Brett Kiyota, Nozomu Yachie, Carl de Boer<sup>&dagger;</sup>",
     "bioRxiv",
     [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v1.abstract")]),
]

JOURNALS = [
    ("2025",
     "Unraveling the regulatory dynamics of bidirectional promoters for modulating gene co-expression and metabolic flux in <i>Saccharomyces cerevisiae</i>",
     "https://academic.oup.com/nar/article/53/11/gkaf511/8160809",
     "Zimo Jin, Yueming Dong, Abdul Muntakim Rafi, Mohsin MD Patwary, Catherine Xu, Morten H. Raadam, Carl de Boer, Codruta Ignea",
     "Nucleic Acids Research",
     [("Journal", "https://academic.oup.com/nar/article/53/11/gkaf511/8160809")]),
    ("2024",
     "A community effort to optimize sequence-based deep learning models of gene regulation",
     "https://www.nature.com/articles/s41587-024-02414-w",
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, Daria Nogina, Dmitry Penzar, Dohoon Lee, Danyeong Lee, Nayeon Kim, Sangyeup Kim, Dohyeon Kim, Yeojin Shin, Il-Youp Kwak, Georgy Meshcheryakov, Andrey Lando, Arsenii Zinkevich, Byeong-Chan Kim, Juhyun Lee, Taein Kang, Eeshit Dhaval Vaishnav, Payman Yadollahpour, Random Promoter DREAM Challenge Consortium, Sun Kim, Jake Albrecht, Aviv Regev, Wuming Gong, Ivan V. Kulakovskiy, Pablo Meyer, Carl de Boer<sup>&dagger;</sup>",
     "Nature Biotechnology",
     [("Journal", "https://www.nature.com/articles/s41587-024-02414-w")]),
    ("2024",
     "Biochemical activity is the default DNA state in eukaryotes",
     "https://www.nature.com/articles/s41594-024-01235-4",
     "Ishika Luthra, Xinyi E Chen, Cassandra Jensen, Asfar Lathif Salaudeen, Abdul Muntakim Rafi, Carl G de Boer",
     "Nature Structural &amp; Molecular Biology",
     [("Journal", "https://www.nature.com/articles/s41594-024-01235-4")]),
    ("2023",
     "LegNet: a best-in-class deep learning model for short DNA regulatory regions",
     "https://academic.oup.com/bioinformatics/article/39/8/btad457/7230784",
     "Dmitry Penzar, Daria Nogina, Elizaveta Noskova, Arsenii Zinkevich, Georgy Meshcheryakov, Andrey Lando, Abdul Muntakim Rafi, Carl de Boer, Ivan V. Kulakovskiy",
     "Bioinformatics",
     [("Journal", "https://academic.oup.com/bioinformatics/article/39/8/btad457/7230784")]),
    ("2023",
     "GIL: A Python package for designing custom indexing primers",
     "https://academic.oup.com/bioinformatics/article/39/6/btad328/7174142",
     "Nicholas Mateyko, Omar Tariq, Xinyi E Chen, Will Cheney, Asfar Lathif Salaudeen, Ishika Luthra, Najmeh Nikpour, Abdul Muntakim Rafi, Hadis Kamali Deghan, Cassandra Jensen, Carl de Boer",
     "Bioinformatics",
     [("Journal", "https://academic.oup.com/bioinformatics/article/39/6/btad328/7174142")]),
    ("2021",
     "RemNet: remnant convolutional neural network for camera model identification",
     "https://link.springer.com/article/10.1007/s00521-020-05220-y",
     "Abdul Muntakim Rafi, Thamidul Islam Tonmoy, Uday Kamal, Jonathan Wu, Md. Kamrul Hasan",
     "Neural Computing and Applications",
     [("Journal", "https://link.springer.com/article/10.1007/s00521-020-05220-y")]),
]

CONFERENCES = [
    ("2020",
     "Lung cancer tumor region segmentation using recurrent 3D-DenseUNet",
     "https://link.springer.com/chapter/10.1007/978-3-030-62469-9_4",
     "Uday Kamal, Abdul Muntakim Rafi, Rakibul Hoque, Jonathan Wu, Md. Kamrul Hasan",
     "Second International Workshop on Thoracic Image Analysis, MICCAI 2020",
     [("Paper", "https://link.springer.com/chapter/10.1007/978-3-030-62469-9_4")]),
    ("2020",
     "Understanding global reaction to the recent outbreaks of COVID-19: insights from Instagram data analysis",
     "https://dl.acm.org/doi/10.1109/SMC42975.2020.9283376",
     "Abdul Muntakim Rafi<sup>*</sup>, Shivang Rana<sup>*</sup>, Rajwinder Kaur<sup>*</sup>, Jonathan Wu, Pooya Moradian Zadeh",
     "IEEE International Conference on Systems, Man, and Cybernetics",
     [("Paper", "https://dl.acm.org/doi/10.1109/SMC42975.2020.9283376")]),
    ("2020",
     "L2-constrained RemNet for camera model identification and image manipulation detection",
     "https://link.springer.com/chapter/10.1007/978-3-030-66823-5_16",
     "Abdul Muntakim Rafi, Jonathan Wu, Md. Kamrul Hasan",
     "Advances in Image Manipulation workshop, ECCV 2020",
     [("Paper", "https://link.springer.com/chapter/10.1007/978-3-030-66823-5_16")]),
    ("2019",
     "Application of DenseNet in camera model identification and post-processing detection",
     "https://openaccess.thecvf.com/content_CVPRW_2019/papers/Media%20Forensics/Rafi_Application_of_DenseNet_in_Camera_Model_Identification_and_Post-processing_Detection_CVPRW_2019_paper.pdf",
     "Abdul Muntakim Rafi, Uday Kamal, Rakibul Hoque, Abid Abrar, Sowmitra Das, Robert Laganiere, Md. Kamrul Hasan",
     "CVPR 2019 Workshops, Long Beach, United States",
     [("PDF", "https://openaccess.thecvf.com/content_CVPRW_2019/papers/Media%20Forensics/Rafi_Application_of_DenseNet_in_Camera_Model_Identification_and_Post-processing_Detection_CVPRW_2019_paper.pdf")]),
    ("2019",
     "Image-based Bengali sign language alphabet recognition for the deaf community",
     "https://ieeexplore.ieee.org/abstract/document/9033031",
     "Abdul Muntakim Rafi, Nowshin Nawal, Nur Sultan Nazar Bayev, Lusain Nima, Celia Shahnaz, Shaikh Anowarul Fattah",
     "IEEE Global Humanitarian Technology Conference (GHTC), Seattle, United States",
     [("Paper", "https://ieeexplore.ieee.org/abstract/document/9033031")]),
]


def render_pubs(items):
    out = []
    for year, title, url, auth, venue, links in items:
        head_html = ('<a href="%s" target="_blank" rel="noopener">%s</a>' % (url, title)) if url else title
        link_html = ""
        if links:
            link_html = '\n        <div class="pub__links">%s</div>' % "".join(
                '<a class="pub__link" href="%s" target="_blank" rel="noopener">%s</a>' % (u, l) for l, u in links)
        out.append("""      <article class="pub">
        <p class="pub__year">{year}</p>
        <div class="pub__body">
          <h3 class="pub__title">{title}</h3>
          <p class="pub__authors">{authors}</p>
          <p class="pub__venue">{venue}</p>{links}
        </div>
      </article>""".format(year=year, title=head_html, authors=authors(auth), venue=venue, links=link_html))
    return "\n".join(out)


# (years, title, [venue, ...])
TALKS = [
    ("2026", "Characterizing homology-induced data leakage and memorization in genome-trained sequence models", [
        "Models, Inference &amp; Algorithms (MIA) Seminar, Broad Institute of MIT and Harvard, Cambridge, United States",
        "MASSIV 1.0: The Meeting for Advanced Synthetic Biology and Systems Bioengineering, Vancouver, Canada",
        "UBC Life Sciences Symposium 2026, Vancouver, Canada <em>(upcoming)</em>",
    ]),
    ("2025", "From inflated benchmarks to trustworthy predictions: addressing reliability in genomic models", [
        "Biomedical Horizons Seminar Series, IBM Thomas J. Watson Research Center, New York, United States",
    ]),
    ("2024&ndash;2025", "Detecting and avoiding homology-based data leakage in genome-trained sequence models", [
        "AI in Molecular Biology, Keystone Symposia, Santa Fe, United States",
        "ISMB/ECCB 2025, Liverpool, United Kingdom",
        "Kipoi Seminar <em>(online)</em>",
        "IGVF Consortium, Machine Learning Focus Group Journal Club <em>(online)</em>",
        "Deep Learning in Genomics Journal Club, Johns Hopkins University <em>(online)</em>",
        "Kundaje Lab Journal Club, Stanford University, Stanford, United States",
        "Kelley group Journal Club, Calico Life Sciences, South San Francisco, United States",
    ]),
    ("2025", "Beyond the genome: engineering and modeling synthetic DNA to uncover cis-regulatory logic", [
        "Tom Ellis Lab, Imperial College London, London, United Kingdom",
    ]),
    ("2025", "A community effort to optimize sequence-based deep learning models of gene regulation", [
        "Genentech, internal seminar <em>(online)</em>",
        "Biological Data Science, Cold Spring Harbor Laboratory, New York, United States",
        "London SynBio Network Meeting, Imperial College London, London, United Kingdom",
    ]),
    ("2024", "Evaluation and optimization of sequence-based gene regulatory deep learning models", [
        "Pacific Northwest Yeast Club Meeting, Fred Hutchinson Cancer Center, Seattle, United States",
    ]),
    ("2022", "Predicting gene expression using random promoter sequences &mdash; challenge overview", [
        "14th RECOMB/ISCB Conference on Regulatory &amp; Systems Genomics with DREAM Challenges, Las Vegas, United States",
    ]),
    ("2021", "Tumor segmentation from CT scans using deep learning", [
        "Guest lecture, ELEC 8280: Image Processing, University of Windsor, Windsor, Canada",
    ]),
    ("2020", "L2-constrained RemNet for camera model identification and image manipulation detection", [
        "Advances in Image Manipulation Workshop, ECCV 2020 <em>(online)</em>",
    ]),
    ("2020", "Lung cancer tumor region segmentation using recurrent 3D-DenseUNet", [
        "Second International Workshop on Thoracic Image Analysis, MICCAI 2020 <em>(online)</em>",
    ]),
    ("2018", "IEEE SPS Video and Image Processing Cup 2018 &mdash; final round", [
        "IEEE International Conference on Image Processing (ICIP), Athens, Greece",
    ]),
    ("2018", "Shongket: Bengali sign language alphabet interpreter for the deaf community in Bangladesh", [
        "4th IEEE WIECON-ECE Conference, Thailand <em>(online)</em>",
    ]),
]

POSTERS = [
    ("2026", "gRely: Reliability estimation of variant effect predictions for genome-trained sequence-to-expression models", [
        "90th Cold Spring Harbor Symposium on Quantitative Biology (AI in Biology), New York, United States <em>(upcoming)</em>",
    ]),
    ("2026", "Evaluation of active learning selection strategies and characterization of informative sequences for sequence-to-expression models", [
        "90th Cold Spring Harbor Symposium on Quantitative Biology (AI in Biology), New York, United States <em>(upcoming)</em>",
    ]),
    ("2024", "Detecting and avoiding homology-based data leakage in genome-trained sequence models", [
        "Biological Data Science, Cold Spring Harbor Laboratory, New York, United States",
        "23rd European Conference on Computational Biology (ECCB), Turku, Finland",
        "Machine Learning in Computational Biology (MLCB), Seattle, United States",
    ]),
    ("2023", "Evaluation and optimization of sequence-based gene regulatory deep learning models", [
        "Machine Learning in Computational Biology (MLCB), Seattle, United States",
        "Kipoi Summit, Zugspitze, Germany",
    ]),
]

WORKSHOPS = [
    ("Oct 2023", "IEEE EMBS Region 9 Conference", "Guadalajara, Mexico",
     "Invited three-hour workshop on designing sequence-based gene regulatory deep learning models."),
    ("Sep 2023", "Advanced Genomics &amp; Genome Engineering Workshop", "Michael Smith Laboratories, UBC",
     "Invited 30-minute lecture on designing sequence-based gene regulatory deep learning models."),
    ("Jun 2023", "Machine Learning for Genome Editing", "Stem Cell Network, Canada <em>(online)</em>",
     "Invited 90-minute workshop: using publicly available ML models for genome editing experiments, training networks on sequence-to-expression data from massively parallel reporter assays, and showing when simpler models outperform complex neural networks."),
]


def render_talks(items):
    out = []
    for year, title, venues in items:
        vs = "\n".join("            <li>%s</li>" % v for v in venues)
        out.append("""      <article class="talk">
        <p class="talk__year">{year}</p>
        <div class="talk__body">
          <h3 class="talk__title">{title}</h3>
          <ul class="talk__venues">
{venues}
          </ul>
        </div>
      </article>""".format(year=year, title=title, venues=vs))
    return "\n".join(out)


def record(name, where=None, when=None, note=None, links=None, items=None):
    """One row of a labelled record: what it was, where, and when."""
    parts = ['        <h3 class="record__name">%s</h3>' % name]
    if where:
        parts.append('        <p class="record__where">%s</p>' % where)
    if note:
        parts.append('        <p class="record__note">%s</p>' % note)
    if items:
        lis = "".join("<li>%s</li>" % i for i in items)
        parts.append('        <ul class="itemlist">%s</ul>' % lis)
    if links:
        parts.append('        <p class="record__links">%s</p>' % "".join(
            '<a class="pub__link" href="%s" target="_blank" rel="noopener">%s</a>' % (u, l) for l, u in links))
    when_html = '\n      <p class="record__when">%s</p>' % when if when else ""
    return """    <article class="record">
      <div class="record__main">
{body}
      </div>{when}
    </article>""".format(body="\n".join(parts), when=when_html)


TOPICS = [
    "Applied machine learning",
    "Computational biology",
    "Sequence-to-expression models",
    "Regulatory genomics",
    "Large-scale DNA synthesis",
    "Massively parallel reporter assays",
    "Active learning",
    "Lab-in-the-loop experiments",
    "Experimental automation",
    "Sequence design",
    "Deep learning",
    "Model interpretation",
    "Simulation of cis-regulation",
    "Model reliability",
    "Variant effect prediction",
    "Data leakage",
    "Benchmark design",
]

THEMES = [
    ("How do we generate the data?",
     "A model can only be as good as the data behind it, and in biology the experiment is where that stops scaling. I design libraries in which each new data point carries information the dataset does not already hold, and synthesize them at a throughput that makes the next model worth training."),
    ("How do we train the best models?",
     "Architecture, objective, augmentation, and the dozens of small decisions in between. The Random Promoter DREAM Challenge turned the independent attempts of roughly 300 scientists into one controlled comparison of which of those decisions actually matter."),
    ("What have the models learned?",
     "A model that predicts well is a hypothesis about the mechanism underneath &mdash; but only if it has learned causal structure rather than correlations the assay happened to leave behind. Leakage between training and test data makes the two indistinguishable on a benchmark."),
    ("Can we trust a single prediction?",
     "An aggregate benchmark number says nothing about the case in front of you, and that is the one that matters wherever a model is actually deployed. I work on per-prediction reliability estimates, so that a model can say when it does not know."),
    ("Can we trust how we read them?",
     "Attribution and perturbation methods are instruments in their own right, and largely untested ones. A confident, accurate model read through a broken lens is worse than no model at all."),
]

TABS = [
    ("research.html", "Research", "The five questions, the projects behind them, and the funding."),
    ("publications.html", "Publications", "Journal articles, conference papers and preprints."),
    ("talks.html", "Talks", "Invited talks, posters and workshops I have run."),
    ("teaching.html", "Teaching", "Courses I have taught and the students I have supervised."),
    ("service.html", "Service", "Peer review, programme committees and community work."),
    ("cv.html", "CV", "Education, positions, awards and the PDF."),
]

def home():
    topics = "\n".join("          <li>%s</li>" % t for t in TOPICS)
    themes = "\n".join(
        '        <article class="theme">\n          <h3>%s</h3>\n          <p>%s</p>\n        </article>' % (t, d)
        for t, d in THEMES)
    tabs = "\n".join(
        '        <a class="cardlink" href="%s">\n'
        '          <span class="cardlink__label">%s</span>\n'
        '          <span class="cardlink__text">%s</span>\n'
        '          <span class="cardlink__arrow" aria-hidden="true">&rarr;</span>\n'
        '        </a>' % (h, l, d) for h, l, d in TABS)

    return """
<section class="hero wrap" id="top">
    <div class="hero__grid">
      <div class="hero__thesis">
        <p class="eyebrow">{role}</p>
        <h1>To benefit from scaling laws in biology, <em>we need the right kind of data.</em></h1>
        <p class="hero__mission">I am a PhD candidate in Biomedical Engineering at the University of British Columbia, in the de Boer Lab. Models of gene regulation, like any predictive model, improve with the data behind them &mdash; and in biology that data has to come from experiments, which do not get cheaper the way compute does. The ceiling on these models is not the architecture; it is how fast we can generate data worth training on.</p>
        <p class="hero__mission">I work on the technologies that move that ceiling. I design experiments that synthesize libraries in which every new data point is informative rather than redundant, at a throughput high enough to train deep learning models and to benefit from the way they scale.</p>
        <p class="hero__mission">But volume is only half of it. Every experiment carries its own bias, and a model will fit that bias as readily as the biology &mdash; so the rest of my work is on models that learn causal structure rather than the correlations an assay left behind, and on knowing when to trust a prediction and the interpretation we draw from it. Scale is what makes these models possible; trust is what makes them worth using.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="{cv}" target="_blank" rel="noopener">Curriculum vitae (PDF)</a>
          <a class="btn btn--ghost" href="publications.html">Publications</a>
        </div>
        <p class="status">
          <span class="status__dot" aria-hidden="true"></span>
          <span><strong>I am always looking for students to work with.</strong> I have supervised several Co-op students in the de Boer Lab, and motivated undergraduates and high-school students are welcome to <a href="mailto:{email}">get in touch</a>.</span>
        </p>
        <p class="hero__note">Vancouver, Canada<br>Previously: Genentech</p>
      </div>

      <div class="hero__aside">
        <div class="portrait">
          <img src="assets/img/portrait.jpg" alt="{name}" width="720" height="720">
        </div>
        <dl class="facts">
          <div class="fact"><dt>Position</dt><dd>PhD candidate, Biomedical Engineering</dd></div>
          <div class="fact"><dt>Lab</dt><dd>de Boer Lab, School of Biomedical Engineering, UBC</dd></div>
          <div class="fact"><dt>Since</dt><dd>2021</dd></div>
          <div class="fact"><dt>Before</dt><dd>MASc, University of Windsor &middot; BSc, BUET</dd></div>
        </dl>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Current work</p>
        <h2>What I work on.</h2>
        <p class="lede">A model is bounded by its data. Our ability to report how much it has learned is bounded by how honestly it was tested. What we can conclude from it is bounded by the tools we read it with. And clinical deployment is bounded by how far we can trust an individual prediction.</p>
      </div>
      <div class="themes">
{themes}
      </div>

      <div class="fieldindex" style="margin-top: clamp(2.5rem, 5vw, 3.5rem);">
        <div class="fieldindex__head">
          <p class="eyebrow">Topics I have worked on</p>
          <p class="fieldindex__count">{ntopics} entries</p>
        </div>
        <ul class="fieldindex__list">
{topics}
        </ul>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Output</p>
        <h2>The record so far.</h2>
      </div>
      <dl class="figures">
        <div class="figure"><dt>Peer-reviewed papers</dt><dd>{npeer}</dd></div>
        <div class="figure"><dt>Preprints &amp; in preparation</dt><dd>{npre}</dd></div>
        <div class="figure"><dt>Invited talks</dt><dd>{ntalks}</dd></div>
        <div class="figure"><dt>Co-op students supervised</dt><dd>5</dd></div>
      </dl>
      <p class="hero__actions"><a class="btn btn--ghost" href="publications.html">All publications</a></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Elsewhere on this site</p>
        <h2>The rest of it.</h2>
      </div>
      <div>
{tabs}
      </div>
    </div>
  </section>
""".format(role=ROLE, cv=CV_PDF, email=EMAIL, name=NAME, themes=themes, topics=topics,
           ntopics=len(TOPICS), npeer=len(JOURNALS) + len(CONFERENCES), npre=len(PREPRINTS),
           ntalks=len(TALKS), tabs=tabs)


RESEARCH_THEMES = [
    ("How do we generate the data?",
     "Informative sequence libraries, at a scale worth training on",
     "Compute scales; wet-lab experiments do not. That asymmetry, not architecture, is what caps models of gene regulation. So the question I spend most time on is how to make data faster than the field currently can &mdash; and how to make sure the extra data is worth having. A library of a million sequences that are all variations on the same theme teaches a model far less than a tenth as many chosen to disagree with it. I work on designing libraries where each new sequence carries information the library does not already hold, and on automating synthesis and measurement so that designing them well actually pays off."),
    ("How do we train the best models?",
     "Which design decisions actually matter",
     "Architecture, objective, augmentation, tokenisation, how the reverse strand is handled, what counts as a replicate &mdash; a published model bundles dozens of these together, and a single paper comparing two of them settles very little. The Random Promoter DREAM Challenge was an attempt to settle some of it in public: roughly 300 scientists building models independently against one held-out measurement, then a controlled analysis of which of their choices explained the differences."),
    ("What have the models learned?",
     "Causal structure, or the shape of the training set",
     "A model that predicts well is only useful as a hypothesis about regulatory grammar if what it learned was regulation. Every assay carries its own biases, and a model will happily fit those instead &mdash; a spurious correlation and a causal mechanism look identical from the loss curve. Homology makes this worse: sequences sharing evolutionary history land on both sides of a train/test split, and a model that merely recognises them scores exactly like one that understands them. Separating the two is a prerequisite for every claim made from a model&rsquo;s internals, and it is why a good deal of reported progress in this field is really measurement error in the benchmark."),
    ("Can we trust a single prediction?",
     "Reliability per prediction, not per benchmark",
     "An aggregate correlation over a test set says nothing about the variant actually in front of you, which is the thing anyone using these models cares about. A model that is right on average and silently wrong on the cases you are asking about is worse than useless. I work on estimating reliability for individual predictions, so that a model has a way of saying when it does not know."),
    ("Can we trust how we read them?",
     "The interpretation tools are instruments too",
     "Attribution methods, in-silico mutagenesis and the rest of the interpretation toolkit are themselves models, and they are much less tested than the networks they are pointed at. If the lens is distorted, a confident and accurate model still yields a wrong biological conclusion &mdash; and nothing in the usual benchmark would catch it."),
]

RESEARCH_POSITIONS = [
    ("Graduate Research Assistant, de Boer Lab",
     "School of Biomedical Engineering, University of British Columbia, Vancouver, Canada",
     "May 2021 &ndash; present", None),
    ("Graduate Research Assistant, Centre for Computer Vision and Deep Learning",
     "Department of Electrical and Computer Engineering, University of Windsor, Windsor, Canada",
     "Aug 2019 &ndash; Mar 2021", None),
    ("Research Assistant, Digital Signal Processing Research Laboratory",
     "Department of Electrical and Electronic Engineering, BUET, Dhaka, Bangladesh",
     "Oct 2018 &ndash; Mar 2019", None),
]

# (title, status, pill class, when, description, [(label, url), ...])
# Descriptions marked below as derived-from-title are placeholders taken from
# the grant title alone and should be replaced with the real summary.
WORK = [
    ("Informative sequence libraries", "In preparation", "pill--green", "2024 &ndash; present",
     "Which sequences are worth making next? We put active learning selection strategies against each other on sequence-to-expression data and characterise what actually makes a sequence informative &mdash; so that a library grows in information rather than only in size. With Justin Qian, Emmanuel Cazottes and Carl de Boer.",
     []),
    ("Continual improvement of gene regulatory models", "Ongoing", "pill--live", "2025 &ndash; 2026",
     "Keeping a sequence-to-expression model improving as new measurements arrive, instead of freezing it at the dataset it happened to be trained on. Supported by priority GPU access from the Digital Research Alliance of Canada.",
     []),
    ("gRely &mdash; reliability of variant effect predictions", "In preparation", "pill--green", "2025 &ndash; present",
     "Benchmark performance in aggregate tells you nothing about whether to trust the prediction for one particular variant. gRely estimates reliability per prediction for genome-trained sequence-to-expression models. Begun during my internship at Genentech, with G&ouml;k&ccedil;en Eraslan and Kipper Fletez-Brant.",
     []),
    ("Homology-based data leakage", "Preprint", "pill--green", "2024 &ndash; 2025",
     "Sequences that share evolutionary history end up on both sides of a train/test split, and the benchmark then rewards a model for recognising them rather than understanding them. We measured how far this inflates reported performance across genome-trained sequence models, and gave a practical way to detect and avoid it.",
     [("Preprint", "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v1.abstract")]),
    ("Random Promoter DREAM Challenge", "Published", "pill--muted", "2022 &ndash; 2024",
     "An open competition to predict expression from random promoter sequences: over 100 teams, roughly 300 scientists, 75+ universities and companies. I was the only graduate student on the organising committee, ran daily operations, and led the analysis that turned all of those independently built models into one controlled account of which design decisions matter.",
     [("Nature Biotechnology", "https://www.nature.com/articles/s41587-024-02414-w")]),
    ("Yorzoi", "Preprint", "pill--green", "2024 &ndash; 2025",
     "Predicting RNA-seq coverage across the yeast genome from sequence alone &mdash; a whole-genome readout rather than one number per construct. With Timon Schneider and the Ellis lab at Imperial College London.",
     [("Preprint", "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract")]),
    ("Lossless preprocessing of the sequence and expression space", "Completed", "pill--muted", "2023",
     "Preprocessing routinely throws away information before a model ever sees it. This project asked how much of the sequence and expression space can be carried through to training intact. Funded by the School of Biomedical Engineering at UBC.",
     []),
    ("Selection on human gene expression", "Completed", "pill--muted", "2022 &ndash; 2024",
     "Using sequence-to-expression models to ask which regulatory variation natural selection has acted on in humans. Supported by priority GPU access from the Digital Research Alliance of Canada.",
     []),
]

# (title, when, source, PI, funding, role)
PROJECTS = [
    ("Continual improvement of gene regulatory models", "2025 &ndash; 2026",
     "The Digital Research Alliance of Canada", "Carl de Boer",
     "Priority access to GPUs", "Co-wrote the proposal"),
    ("Evaluation, optimization and continual improvement of sequence-based cis-regulatory models",
     "Aug 2023 &ndash; Jun 2024",
     "Advanced Research Computing, UBC", "Carl de Boer",
     "20,000 CAD in Microsoft Azure credit", "Co-applicant; wrote the proposal"),
    ("Lossless preprocessing of the sequence and expression space to improve sequence-based gene regulatory models",
     "May &ndash; Aug 2023",
     "School of Biomedical Engineering, UBC", "Carl de Boer", "6,000 CAD",
     "Co-applicant; wrote the proposal and hired a Co-op student through the grant"),
    ("Random Promoter DREAM Challenge 2022", "May &ndash; Jul 2022",
     "TPU Research Cloud, Google",
     "Carl de Boer (UBC), Pablo Meyer (IBM Research), Jake Albrecht (Sage Bionetworks)",
     "50 TPU quotas", "Sole graduate student on the organising committee"),
    ("Identifying selection on human gene expression with gene regulatory models", "2022 &ndash; 2024",
     "The Digital Research Alliance of Canada", "Carl de Boer",
     "Priority access to GPUs", "Co-wrote the proposal"),
    ("Efficient edge inference benchmarking for AI-driven applications", "Nov 2020 &ndash; Mar 2021",
     "Mitacs Accelerate", "Jonathan Wu", "15,000 CAD", "Sole co-applicant; wrote the proposal"),
    ("Spatio-temporal human activity recognition on manufacturing floors", "Oct 2019 &ndash; Apr 2020",
     "Mitacs Accelerate", "Jonathan Wu", "22,500 CAD", "Co-applicant; assisted with proposal writing"),
]


def render_work(items):
    out = []
    for title, status, pill, when, text, links in items:
        link_html = ""
        if links:
            link_html = '\n          <p class="project__links">%s</p>' % "".join(
                '<a class="pub__link" href="%s" target="_blank" rel="noopener">%s</a>' % (u, l)
                for l, u in links)
        out.append("""        <article class="project">
          <div class="project__head">
            <h3 class="project__title">{title}</h3>
            <span class="pill {pill}">{status}</span>
          </div>
          <p class="project__when">{when}</p>
          <p class="project__text">{text}</p>{links}
        </article>""".format(title=title, pill=pill, status=status, when=when,
                             text=text, links=link_html))
    return "\n".join(out)


def research():
    themes = "\n".join(
        record(title, where=sub, note=body) for title, sub, body in RESEARCH_THEMES)
    positions = "\n".join(
        record(title, where=where, when=when, note=note)
        for title, where, when, note in RESEARCH_POSITIONS)
    projects = "\n".join(
        record(t, where="%s &middot; PI: %s" % (s, p),
               when=w, note="%s. %s." % (f, r))
        for t, w, s, p, f, r in PROJECTS)

    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Research</p>
        <h1>Make the data scale. Then find out what the model really knows.</h1>
        <p class="lede">Designing informative sequence libraries and automating the experiments that read them &mdash; and testing, honestly, how much of what a model appears to have learned from them is real.</p>
      </div>
      <div class="prose prose--wide">
        <p>Regulation is written into the genome, and a model that reads it well is useful twice over: as a predictor, and as a hypothesis about the grammar itself. Both uses are capped by the same thing. <strong>Data is the binding constraint in this field</strong>, and biology is the one place where it does not get cheaper on its own &mdash; compute scales, sequencing scales, the experiment does not.</p>
        <p>So the work runs in two directions. One is making data faster and making it count: libraries designed so that each new sequence disagrees with what the model already believes, rather than confirming it, and enough automation that designing them well is worth the effort. Noisy measurements at scale beat clean measurements you cannot afford.</p>
        <p>The other is refusing to take the resulting models at face value. Much of what looks like progress here is <strong>measurement error in the benchmark</strong> &mdash; sequences sharing evolutionary history on both sides of a train/test split, performance going up, nothing learned. Beyond that sits the question of whether an individual prediction can be trusted, and whether the tools we use to read a model are themselves telling us the truth.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Themes</p>
        <h2>What I actually spend time on.</h2>
      </div>
      <div class="records">
{themes}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Projects</p>
        <h2>What I have worked on.</h2>
        <p class="lede">Including the work that has not been written up yet. Anything with a paper behind it links to one.</p>
      </div>
      <div class="projects">
{work}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Positions</p>
        <h2>Where the work has been done.</h2>
      </div>
      <div class="records">
{positions}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Funding</p>
        <h2>Grants and compute.</h2>
        <p class="lede">Proposals I wrote or co-wrote, with the role I held on each.</p>
      </div>
      <div class="records">
{projects}
      </div>
    </div>
  </section>
""".format(themes=themes, work=render_work(WORK), positions=positions, projects=projects)


def publications():
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Publications</p>
        <h1>Papers, preprints and work in progress.</h1>
        <p class="lede">Also on <a href="{scholar}" target="_blank" rel="noopener">Google Scholar</a> and <a href="{rg}" target="_blank" rel="noopener">ResearchGate</a>.</p>
      </div>
      <dl class="figures">
        <div class="figure"><dt>Journal articles</dt><dd>{njournal}</dd></div>
        <div class="figure"><dt>Conference papers</dt><dd>{nconf}</dd></div>
        <div class="figure"><dt>Preprints &amp; in preparation</dt><dd>{npre}</dd></div>
      </dl>

      <div class="pubs">
        <div class="grouplabel"><p class="eyebrow">Preprints and in preparation</p><span class="fieldindex__count">{npre} entries</span></div>
{preprints}
        <div class="grouplabel"><p class="eyebrow">Journal articles</p><span class="fieldindex__count">{njournal} entries</span></div>
{journals}
        <div class="grouplabel"><p class="eyebrow">Conference papers</p><span class="fieldindex__count">{nconf} entries</span></div>
{conferences}
      </div>
      <p class="legend"><sup>*</sup> Equal contribution &nbsp;&middot;&nbsp; <sup>&dagger;</sup> Corresponding author</p>
    </div>
  </section>
""".format(scholar=SCHOLAR, rg=RESEARCHGATE,
           npre=len(PREPRINTS), njournal=len(JOURNALS), nconf=len(CONFERENCES),
           preprints=render_pubs(PREPRINTS), journals=render_pubs(JOURNALS),
           conferences=render_pubs(CONFERENCES))


def talks():
    workshops = "\n".join(
        record(title, where=where, when=when, note=note) for when, title, where, note in WORKSHOPS)
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Talks</p>
        <h1>Invited talks, posters and workshops.</h1>
        <p class="lede">A line of work usually gets presented several times before it is written up. Each entry below lists the venues it was given at.</p>
      </div>
      <div class="talks">
{talks}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Posters</p>
        <h2>Selected posters.</h2>
      </div>
      <div class="talks">
{posters}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Workshops</p>
        <h2>Workshops I have run.</h2>
        <p class="lede">Hands-on sessions on building and using sequence-based gene regulatory models.</p>
      </div>
      <div class="records">
{workshops}
      </div>
    </div>
  </section>
""".format(talks=render_talks(TALKS), posters=render_talks(POSTERS), workshops=workshops)


MDS = "https://ubc-mds.github.io/course-descriptions/"
MDS_COURSES = [
    ("DSCI 571: Supervised Learning I", MDS + "DSCI_571_sup-learn-1/"),
    ("DSCI 572: Supervised Learning II", MDS + "DSCI_572_sup-learn-2/"),
    ("DSCI 562: Regression II", "https://ubc-mds.github.io/DSCI_562_regr-2/"),
    ("DSCI 553: Statistical Inference and Computation II", "https://github.com/UBC-MDS/DSCI_553_stat-inf-2"),
    ("DSCI 554: Experimentation and Causal Inference", MDS + "DSCI_554_experi-catic/"),
    ("DSCI 573: Feature and Model Selection", MDS + "DSCI_573_feat-model-tic/"),
    ("DSCI 512: Algorithms and Data Structures", MDS + "DSCI_512_alg-data-struct/"),
    ("DSCI 531: Data Visualization I", MDS + "DSCI_531_viz-1/"),
    ("DSCI 522: Data Science Workflows", MDS + "DSCI_522_dsci-workflows/"),
    ("DSCI 525: Web and Cloud Computing", MDS + "DSCI_525_web-cloud-comp/"),
    ("DSCI 521: Computing Platforms for Data Science", MDS + "DSCI_521_platforms-dsci/"),
]


def teaching():
    mds_items = ['<li><a href="%s" target="_blank" rel="noopener">%s</a></li>' % (u, n) for n, u in MDS_COURSES]
    courses = "\n".join([
        record('Graduate Teaching Assistant &mdash; <a href="https://masterdatascience.ubc.ca/" target="_blank" rel="noopener">Master of Data Science</a>',
               where="University of British Columbia", when="Sep 2021 &ndash; Dec 2024",
               note="Eleven courses across the MDS curriculum, from supervised learning and regression through workflows, visualisation and cloud computing.",
               items=[i[4:-5] for i in mds_items]),
        record('Graduate Teaching Assistant &mdash; <a href="https://www.biology.ubc.ca/" target="_blank" rel="noopener">Biology Program</a>',
               where="University of British Columbia", when="May &ndash; Jun 2022",
               items=["BIOL 234: Fundamentals of Genetics"]),
        record('Graduate Teaching Assistant &mdash; <a href="https://www.uwindsor.ca/engineering/electrical/" target="_blank" rel="noopener">Electrical and Computer Engineering</a>',
               where="University of Windsor", when="Jan &ndash; Dec 2020",
               items=["ELEC 8330: Computational Intelligence", "GENG 2320: Engineering Software Fundamentals"]),
    ])

    mentorship = "\n".join([
        record('<a href="https://bsri-bd.github.io/" target="_blank" rel="noopener">Bangladeshi Student Research Initiative</a>',
               where="Founder", when="2024 &ndash; present",
               note="A non-profit connecting undergraduate and postgraduate students in Bangladesh with Bangladeshi researchers in academia and industry abroad, through free mentorship programmes."),
        record("de Boer Lab",
               where="School of Biomedical Engineering, UBC", when="2023 &ndash; present",
               note="Sole supervisor for five Co-op students on self-designed research projects; one of them went on to receive SBME Synergy funding. I also mentor junior PhD students in the lab."),
        record("Talaria Summer Institute",
               where="Genomics sequence analysis project", when="2023",
               note="Supervised a high-school student through TSI, a free summer STEM research mentorship programme for female and genderqueer students."),
        record("SUS&ndash;GSS Mentorship Program",
               where="University of British Columbia", when="2022",
               note="Mentored second-year undergraduates on professional development."),
    ])

    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Teaching</p>
        <h1>Courses taught, and students supervised.</h1>
        <p class="lede">Fourteen course offerings across three departments, and a handful of students whose projects were their own.</p>
      </div>
      <p class="status">
        <span class="status__dot" aria-hidden="true"></span>
        <span><strong>I am always looking for students to work with.</strong> Motivated undergraduates and high-school students interested in machine learning for genomics are welcome to <a href="mailto:{email}">write to me</a>.</span>
      </p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Teaching assistantships</p>
        <h2>Courses.</h2>
      </div>
      <div class="records">
{courses}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Mentorship</p>
        <h2>Students and programmes.</h2>
      </div>
      <div class="records">
{mentorship}
      </div>
    </div>
  </section>
""".format(email=EMAIL, courses=courses, mentorship=mentorship)


REVIEW_INDEPENDENT = [
    ("Nature Communications", "1 paper"),
    ("Bioinformatics", "1 paper"),
    ("Neurocomputing", "4 papers"),
    ("Computational and Structural Biotechnology Journal", "1 paper"),
    ("Data in Brief", "1 paper"),
    ("Journal of Real-Time Image Processing", "1 paper"),
    ("Cyber-systems and Robotics", "1 paper"),
    ("ISMB 2026", "1 paper"),
    ("Machine Learning in Computational Biology 2025", "3 extended abstracts"),
    ("Generative AI in Genomics (Gen<sup>2</sup>) workshop, ICLR 2026", "1 paper"),
]

REVIEW_CO = [
    ("Nature", "2 papers"),
    ("Nature Genetics", "1 paper"),
    ("PNAS", "1 paper"),
    ("Genome Biology", "1 paper"),
    ("Bioinformatics", "1 paper"),
]

SERVICE_ROLES = [
    ("Programme committee member, Machine Learning in Computational and Systems Biology track",
     "ISMB conference", "2026", None),
    ("Scientific programme committee member",
     "Machine Learning in Computational Biology (MLCB) conference", "2025", None),
    ("BSc thesis committee member",
     "Faculty of Science, University of British Columbia", "2025", None),
]

COMMUNITY = [
    ('Founder, <a href="https://bsri-bd.github.io/" target="_blank" rel="noopener">Bangladeshi Student Research Initiative</a>',
     "A volunteer research network", "2024 &ndash; present",
     "Founded a non-profit that connects students at Bangladeshi universities with Bangladeshi researchers abroad through free mentorship programmes."),
    ("Project manager, SynBio 6.0", "University of British Columbia", "2024",
     "Managed the organisation of a two-day national synthetic biology symposium hosted at UBC, bringing together around 100 Canadian researchers."),
    ("President, Bangladeshi Grad Alliance UBC", "University of British Columbia", "2024 &ndash; 2025",
     "Co-founded the organisation and served as its inaugural President, establishing the first executive committee and running community events for Bangladeshi graduate students."),
    ("Project co-ordinator and organiser, Random Promoter DREAM Challenge", "UBC, IBM Research and Sage Bionetworks", "2022",
     "Co-organised an international competition with over 100 teams &mdash; roughly 300 scientists from 75+ universities and companies &mdash; to build models predicting gene expression from sequence. Ran daily operations as the only graduate student on the organising committee."),
    ("Secretary, Biomedical Engineering Graduate Association", "University of British Columbia", "2021 &ndash; 2022",
     "Organised social and networking events across research groups in the department."),
    ("Graduate student representative, SBME Sustainability Committee", "University of British Columbia", "2021 &ndash; 2022",
     "Represented graduate students in developing initiatives to integrate sustainable practices into the school&rsquo;s operations."),
    ("Assistant Treasurer, IEEE Joint Chapter SP/COM, Windsor Section", "University of Windsor", "2020 &ndash; 2021",
     "Researched and evaluated financing alternatives, and made recommendations supporting chapter operations."),
    ("Vice President, Satyen Bose Science Club", "BUET, Dhaka", "2017 &ndash; 2018",
     "Organised scientific talks, seminars and debates. Assistant General Secretary the year before, co-ordinating event logistics and on-the-ground operations."),
    ("Volunteer tutor", "BUET dormitory canteen, Dhaka &middot; Bholananda Night High School, Sylhet", "2011 &ndash; 2015",
     "Taught literacy to children and adult workers at the university dormitory canteen, and tutored children who worked during the day to support their families."),
]

MEMBERSHIPS = [
    ("Synbio Canada &mdash; Class A voting member", "2024 &ndash; present"),
    ("International Society for Computational Biology (ISCB)", "2022, 2024, 2025"),
    ("IEEE Signal Processing Society", "2018, 2020 &ndash; 2021"),
    ("Institute of Electrical and Electronics Engineers (IEEE)", "2018, 2020 &ndash; 2021"),
]


def reflist(rows):
    return "\n".join("        <li><span>%s</span><span>%s</span></li>" % (a, b) for a, b in rows)


def service():
    roles = "\n".join(record(t, where=w, when=n, note=d) for t, w, n, d in SERVICE_ROLES)
    community = "\n".join(record(t, where=w, when=n, note=d) for t, w, n, d in COMMUNITY)
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Service</p>
        <h1>Reviewing, committees and community work.</h1>
        <p class="lede">The parts of the job that are nobody&rsquo;s job.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Peer review</p>
        <h2>Journals and conferences.</h2>
      </div>
      <div class="cols">
        <div>
          <p class="subhead">As independent reviewer</p>
          <ul class="reflist">
{independent}
          </ul>
        </div>
        <div>
          <p class="subhead">As co-reviewer with my PI</p>
          <ul class="reflist">
{co}
          </ul>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Academic service</p>
        <h2>Committees.</h2>
      </div>
      <div class="records">
{roles}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Community</p>
        <h2>Organising, and giving time.</h2>
      </div>
      <div class="records">
{community}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Memberships</p>
        <h2>Societies.</h2>
      </div>
      <ul class="reflist">
{memberships}
      </ul>
    </div>
  </section>
""".format(independent=reflist(REVIEW_INDEPENDENT), co=reflist(REVIEW_CO),
           roles=roles, community=community, memberships=reflist(MEMBERSHIPS))


EDUCATION = [
    ("Doctor of Philosophy in Biomedical Engineering",
     "University of British Columbia, Vancouver, Canada",
     "2021 &ndash; present",
     "Supervisor: Carl de Boer, Assistant Professor, School of Biomedical Engineering. Cumulative average 88.7/100."),
    ("Master of Applied Science in Electrical Engineering",
     "University of Windsor, Windsor, Canada",
     "2019 &ndash; 2021",
     "Supervisor: Jonathan Wu, Professor, Department of Electrical and Computer Engineering. Cumulative average 91.75/100."),
    ("Bachelor of Science in Electrical and Electronic Engineering",
     "Bangladesh University of Engineering and Technology (BUET), Dhaka, Bangladesh",
     "2014 &ndash; 2018",
     "Supervisor: Md. Kamrul Hasan, Professor, Department of EEE. CGPA 3.47/4.00."),
]

POSITIONS = [
    ('Intern &mdash; Human Genetics, <a href="https://www.gene.com/" target="_blank" rel="noopener">Genentech Inc.</a>',
     "South San Francisco, United States", "Jun &ndash; Aug 2025",
     "Developed reliability estimation methods for sequence-to-expression model predictions."),
    ("Graduate Teaching Assistant, Master of Data Science",
     "University of British Columbia", "Sep 2021 &ndash; Dec 2024",
     'Eleven courses across the MDS curriculum &mdash; <a href="teaching.html">the full list is on the teaching page</a>.'),
    ("Graduate Teaching Assistant, Biology Program",
     "University of British Columbia", "May &ndash; Jun 2022",
     "BIOL 234: Fundamentals of Genetics."),
    ('Mitacs Accelerate Intern, <a href="https://www.lannerinc.com/" target="_blank" rel="noopener">Lanner Electronics Inc.</a>',
     "Canada&rsquo;s premier research internship programme", "Nov 2020 &ndash; Mar 2021",
     "Benchmarked efficient inference of AI-driven applications on edge devices."),
    ("Graduate Teaching Assistant, Electrical and Computer Engineering",
     "University of Windsor", "Jan &ndash; Dec 2020",
     "Engineering Software Fundamentals; Computational Intelligence."),
    ('Mitacs Accelerate Intern, <a href="https://www.i-5o.ai/" target="_blank" rel="noopener">IFIVEO</a>',
     "Windsor, Canada", "Oct 2019 &ndash; Apr 2020",
     "Developed vision-based deep learning models for activity recognition on manufacturing floors: collected data on site, supervised annotation, and deployed models with Amazon SageMaker."),
    ('Machine Learning Engineer, <a href="https://www.revesoft.com/" target="_blank" rel="noopener">REVE Systems Ltd.</a>',
     "Dhaka, Bangladesh", "Mar &ndash; Jul 2019",
     "Designed a real-time Sign2Text translator for Bangla Sign Language."),
]

AWARDS = [
    ("Four Year Doctoral Fellowship (4YF)", "University of British Columbia", "2021 &ndash; 2025",
     "96,000 CAD over four years. UBC&rsquo;s flagship doctoral fellowship, providing funding plus tuition to top PhD students."),
    ("SCN International Travel Award", "Stem Cell Network, Canada", "2025",
     "1,500 CAD. Awarded to trainees to present their work internationally and raise the visibility of Canadian research abroad."),
    ("JXTX + CSHL Biological Data Science Scholarship", "Cold Spring Harbor Laboratory", "2024",
     "1,125 USD. Awarded to six graduate students in genomics and data science for contributions to open science."),
    ("Stem Cell Network Trainee Award", "Stem Cell Network, Canada", "2023",
     "4,000 CAD. One-time stipend awarded to approximately 100 trainees nationally."),
    ("Amgen Pitch Competition &mdash; 3rd place", "School of Biomedical Engineering, UBC", "2023",
     "1,000 CAD."),
    ("PharmaHacks &mdash; 1st place", "Phyla Challenge", "2022",
     "Classification of diseases based on the gut microbiome."),
    ("SBME Graduate Support Initiative Entrance Award", "University of British Columbia", "2021",
     "4,000 CAD. Awarded to top-ranked incoming PhD students in SBME."),
    ("IEEE SPS Video and Image Processing Cup &mdash; 2nd place", "IEEE Signal Processing Society", "2018",
     "2,500 USD. Placed second among 28 international teams."),
    ("IEEE WIECON-ECE Humanitarian Project Competition &mdash; 2nd place", "IEEE", "2018",
     "500 USD."),
    ("Bangladesh Mathematical Olympiad &mdash; Regional Champion", "Bangladesh", "2011 &ndash; 2013", None),
    ("Bangladesh Astro Olympiad &mdash; National 4th", "Bangladesh", "2012", None),
    ("Bangladesh Physics Olympiad &mdash; Regional Champion", "Bangladesh", "2012", None),
    ("Bangladesh Science Olympiad &mdash; National 3rd", "Bangladesh", "2011", None),
]


def cv():
    education = "\n".join(record(t, where=w, when=n, note=d) for t, w, n, d in EDUCATION)
    positions = "\n".join(record(t, where=w, when=n, note=d) for t, w, n, d in POSITIONS)
    awards = "\n".join(record(t, where=w, when=n, note=d) for t, w, n, d in AWARDS)
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Curriculum vitae</p>
        <h1>Education, positions and awards.</h1>
        <p class="lede">The full record, with the PDF below. Publications, talks, teaching and service each have their own page.</p>
      </div>
      <div class="downloads">
        <a class="download" href="{cv}" target="_blank" rel="noopener">
          <span class="download__name">Curriculum vitae</span>
          <span class="download__text">The complete CV: education, research and work experience, publications, talks, posters, funding, service and awards.</span>
          <span class="download__meta">PDF &middot; 6 pages</span>
        </a>
        <a class="download" href="{failure}" target="_blank" rel="noopener">
          <span class="download__name">CV of failures</span>
          <span class="download__text">The rejections, the missed fellowships and the papers that did not land. Most CVs are a survivorship-biased record; this is the other half of mine.</span>
          <span class="download__meta">PDF</span>
        </a>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Education</p>
        <h2>Degrees.</h2>
      </div>
      <div class="records">
{education}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Experience</p>
        <h2>Positions held.</h2>
        <p class="lede">Research positions are listed on the <a href="research.html">research page</a>.</p>
      </div>
      <div class="records">
{positions}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Awards</p>
        <h2>Fellowships, scholarships and competitions.</h2>
      </div>
      <div class="records">
{awards}
      </div>
    </div>
  </section>
""".format(cv=CV_PDF, failure=FAILURE_PDF, education=education, positions=positions, awards=awards)


PAGES = [
    ("index.html", NAME,
     "Abdul Muntakim Rafi is a PhD candidate in Biomedical Engineering at the University of British Columbia, working on informative sequence libraries at scale and on machine learning models of gene regulation built from them.",
     home),
    ("research.html", "Research",
     "Informative sequence library design and experimental automation, sequence-to-expression models, honest benchmarking, per-prediction reliability, and the interpretation tools themselves.",
     research),
    ("publications.html", "Publications",
     "Journal articles, conference papers and preprints by Abdul Muntakim Rafi.",
     publications),
    ("talks.html", "Talks",
     "Invited talks, selected posters and workshops given by Abdul Muntakim Rafi.",
     talks),
    ("teaching.html", "Teaching",
     "Courses taught at UBC and the University of Windsor, and students supervised in the de Boer Lab and beyond.",
     teaching),
    ("service.html", "Service",
     "Peer review, programme committees, memberships and community organising.",
     service),
    ("cv.html", "CV",
     "Education, positions held and awards, with the full CV as a PDF.",
     cv),
]


def main():
    for slug, title, desc, builder in PAGES:
        path = write(slug, title, desc, builder())
        print("wrote %s" % os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
