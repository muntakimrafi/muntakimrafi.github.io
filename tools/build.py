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
LAB = "https://deboer.bme.ubc.ca/"
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
      </div>
    </div>
    <nav class="footer__links" aria-label="Footer">
{links}
    </nav>
  </div>
</footer>

<script src="assets/js/main.js"></script>
</body>
</html>
""".format(name=NAME, social=social, links=links)


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
     "gRely: Reliability for genome-trained sequence-to-function model predictions",
     "https://www.biorxiv.org/content/10.64898/2026.05.23.727431v1",
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, G&ouml;k&ccedil;en Eraslan, Kipper Fletez-Brant<sup>&dagger;</sup>",
     "bioRxiv &middot; under review",
     [("Preprint", "https://www.biorxiv.org/content/10.64898/2026.05.23.727431v1")]),
    ("2026",
     "Evaluation of active learning selection strategies and characterization of informative sequences for sequence-to-expression models",
     "https://www.biorxiv.org/content/10.64898/2026.05.21.727038v1",
     "Justin Qian<sup>*</sup>, Abdul Muntakim Rafi<sup>*&dagger;</sup>, Emmanuel Cazottes<sup>*</sup>, Carl de Boer<sup>&dagger;</sup>",
     "bioRxiv &middot; under review",
     [("Preprint", "https://www.biorxiv.org/content/10.64898/2026.05.21.727038v1"), ("Code", "https://github.com/de-Boer-Lab/nextFrag")]),
    ("2025",
     "Yorzoi: Predicting RNA-seq coverage from DNA sequence in yeast",
     "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract",
     "Timon Schneider, Abdul Muntakim Rafi, Cassandra Jensen, Daniella Liao, Yiren Zhao, Carl de Boer, Tom Ellis",
     "bioRxiv",
     [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract"), ("Code", "https://github.com/Tom-Ellis-Lab/yorzoi")]),
    ("2025",
     "Characterizing homology-induced data leakage and memorization in genome-trained sequence models",
     "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v2",
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, Brett Kiyota, Nozomu Yachie, Carl de Boer<sup>&dagger;</sup>",
     "bioRxiv &middot; under review",
     [("bioRxiv", "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v2"), ("Code", "https://github.com/de-Boer-Lab/hashFrag")]),
]

JOURNALS = [
    ("2025",
     "Unraveling the regulatory dynamics of bidirectional promoters for modulating gene co-expression and metabolic flux in <i>Saccharomyces cerevisiae</i>",
     "https://academic.oup.com/nar/article/53/11/gkaf511/8160809",
     "Zimo Jin, Yueming Dong, Abdul Muntakim Rafi, Mohsin MD Patwary, Catherine Xu, Morten H. Raadam, Carl de Boer, Codruta Ignea",
     "Nucleic Acids Research",
     [("Journal", "https://academic.oup.com/nar/article/53/11/gkaf511/8160809")]),
    ("2025",
     "A community effort to optimize sequence-based deep learning models of gene regulation",
     "https://www.nature.com/articles/s41587-024-02414-w",
     "Abdul Muntakim Rafi<sup>&dagger;</sup>, Daria Nogina, Dmitry Penzar, Dohoon Lee, Danyeong Lee, Nayeon Kim, Sangyeup Kim, Dohyeon Kim, Yeojin Shin, Il-Youp Kwak, Georgy Meshcheryakov, Andrey Lando, Arsenii Zinkevich, Byeong-Chan Kim, Juhyun Lee, Taein Kang, Eeshit Dhaval Vaishnav, Payman Yadollahpour, Random Promoter DREAM Challenge Consortium, Sun Kim, Jake Albrecht, Aviv Regev, Wuming Gong, Ivan V. Kulakovskiy, Pablo Meyer, Carl de Boer<sup>&dagger;</sup>",
     "Nature Biotechnology 43(8):1373&ndash;1383",
     [("Journal", "https://www.nature.com/articles/s41587-024-02414-w"), ("Code", "https://github.com/de-Boer-Lab/random-promoter-dream-challenge-2022")]),
    ("2024",
     "Regulatory activity is the default DNA state in eukaryotes",
     "https://www.nature.com/articles/s41594-024-01235-4",
     "Ishika Luthra, Cassandra Jensen, Xinyi E Chen, Asfar Lathif Salaudeen, Abdul Muntakim Rafi, Carl G de Boer",
     "Nature Structural &amp; Molecular Biology",
     [("Journal", "https://www.nature.com/articles/s41594-024-01235-4"), ("Code", "https://github.com/de-Boer-Lab/RGP")]),
    ("2023",
     "LegNet: a best-in-class deep learning model for short DNA regulatory regions",
     "https://academic.oup.com/bioinformatics/article/39/8/btad457/7230784",
     "Dmitry Penzar, Daria Nogina, Elizaveta Noskova, Arsenii Zinkevich, Georgy Meshcheryakov, Andrey Lando, Abdul Muntakim Rafi, Carl de Boer, Ivan V. Kulakovskiy",
     "Bioinformatics",
     [("Journal", "https://academic.oup.com/bioinformatics/article/39/8/btad457/7230784"), ("Code", "https://github.com/autosome-ru/LegNet")]),
    ("2023",
     "GIL: A Python package for designing custom indexing primers",
     "https://academic.oup.com/bioinformatics/article/39/6/btad328/7174142",
     "Nicholas Mateyko, Omar Tariq, Xinyi E Chen, Will Cheney, Asfar Lathif Salaudeen, Ishika Luthra, Najmeh Nikpour, Abdul Muntakim Rafi, Hadis Kamali Deghan, Cassandra Jensen, Carl de Boer",
     "Bioinformatics",
     [("Journal", "https://academic.oup.com/bioinformatics/article/39/6/btad328/7174142"), ("Code", "https://github.com/de-Boer-Lab/GIL")]),
    ("2021",
     "RemNet: remnant convolutional neural network for camera model identification",
     "https://link.springer.com/article/10.1007/s00521-020-05220-y",
     "Abdul Muntakim Rafi, Thamidul Islam Tonmoy, Uday Kamal, Jonathan Wu, Md. Kamrul Hasan",
     "Neural Computing and Applications",
     [("Journal", "https://link.springer.com/article/10.1007/s00521-020-05220-y"), ("Code", "https://github.com/muntakimrafi/RemNet-remnant-convolutional-neural-network-for-camera-model-identification")]),
]

CONFERENCES = [
    ("2020",
     "Lung cancer tumor region segmentation using recurrent 3D-DenseUNet",
     "https://link.springer.com/chapter/10.1007/978-3-030-62469-9_4",
     "Uday Kamal, Abdul Muntakim Rafi, Rakibul Hoque, Jonathan Wu, Md. Kamrul Hasan",
     "Second International Workshop on Thoracic Image Analysis, MICCAI 2020",
     [("Paper", "https://link.springer.com/chapter/10.1007/978-3-030-62469-9_4"), ("Code", "https://github.com/muntakimrafi/TIA2020-Recurrent-3D-DenseUNet")]),
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
     [("Paper", "https://openaccess.thecvf.com/content_CVPRW_2019/papers/Media%20Forensics/Rafi_Application_of_DenseNet_in_Camera_Model_Identification_and_Post-processing_Detection_CVPRW_2019_paper.pdf"), ("Code", "https://github.com/muntakimrafi/Application-of-DenseNet-in-Camera-Model-Identification-and-Post-processing-Detection")]),
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


# Talks, one entry per occasion rather than one per title, so the venue leads.
# The mark is the venue's logo from assets/img/venues/, or its initials when
# no logo has been added.
# (mark, venue, place, year, topic, note)

_HOMOLOGY = "Characterizing homology-induced data leakage and memorization in genome-trained sequence models"
_TRUST = "From inflated benchmarks to trustworthy predictions: addressing reliability in genomic models"
_LEAKAGE = "Detecting and avoiding homology-based data leakage in genome-trained sequence models"
_DREAM = "A community effort to optimize sequence-based deep learning models of gene regulation"
_EVAL = "Evaluation and optimization of sequence-based gene regulatory deep learning models"
_CHALLENGE = "Predicting gene expression using random promoter sequences &mdash; challenge overview"
_TUMOR = "Tumor segmentation from CT scans using deep learning"
_REMNET = "L2-constrained RemNet for camera model identification and image manipulation detection"
_LUNG = "Lung cancer tumor region segmentation using recurrent 3D-DenseUNet"
_VIPCUP = "IEEE SPS Video and Image Processing Cup 2018 &mdash; final round"
_SHONGKET = "Shongket: Bengali sign language alphabet interpreter for the deaf community in Bangladesh"

INVITED = [
    ("BI", "Models, Inference &amp; Algorithms Seminar", "Broad Institute of MIT and Harvard, Cambridge, United States", "2026", _HOMOLOGY, None),
    ("IBM", "Biomedical Horizons Seminar Series", "IBM Thomas J. Watson Research Center, New York, United States", "2025", _TRUST, None),
    ("LSN", "London SynBio Network Meeting", "Imperial College London, London, United Kingdom", "2025", _DREAM, None),
    ("GNE", "Genentech internal seminar", "South San Francisco, United States", "2025", _DREAM, "Online"),
    ("JHU", "Deep Learning in Genomics Journal Club", "Johns Hopkins University", "2025", _LEAKAGE, "Online"),
    ("IGVF", "IGVF Consortium, Machine Learning Focus Group Journal Club", "IGVF Consortium", "2025", _LEAKAGE, "Online"),
    ("KIP", "Kipoi Seminar", "Kipoi community", "2024", _LEAKAGE, "Online"),
    ("UW", "Guest lecture, ELEC 8280: Image Processing", "University of Windsor, Windsor, Canada", "2021", _TUMOR, None),
]

TALKS = [
    ("MSV", "MASSIV 1.0 &mdash; Advanced Synthetic Biology and Systems Bioengineering", "Vancouver, Canada", "2026", _HOMOLOGY, None),
    ("UBC", "UBC Life Sciences Symposium", "Vancouver, Canada", "2026", _HOMOLOGY, None),
    ("ISMB", "ISMB/ECCB 2025", "Liverpool, United Kingdom", "2025", _LEAKAGE, None),
    ("CSHL", "Biological Data Science", "Cold Spring Harbor Laboratory, New York, United States", "2025", _DREAM, None),
    ("KEY", "AI in Molecular Biology, Keystone Symposia", "Santa Fe, United States", "2025", _LEAKAGE, None),
    ("SU", "Kundaje Lab Journal Club", "Stanford University, Stanford, United States", "2025", _LEAKAGE, None),
    ("CAL", "Kelley Group Journal Club", "Calico Life Sciences, South San Francisco, United States", "2025", _LEAKAGE, None),
    ("FH", "Pacific Northwest Yeast Club Meeting", "Fred Hutchinson Cancer Center, Seattle, United States", "2024", _EVAL, None),
    ("RSG", "14th RECOMB/ISCB Conference on Regulatory &amp; Systems Genomics with DREAM Challenges", "Las Vegas, United States", "2022", _CHALLENGE, None),
    ("ECCV", "Advances in Image Manipulation Workshop, ECCV 2020", "ECCV 2020", "2020", _REMNET, "Online"),
    ("MIC", "Second International Workshop on Thoracic Image Analysis, MICCAI 2020", "MICCAI 2020", "2020", _LUNG, "Online"),
    ("IEEE", "IEEE International Conference on Image Processing", "Athens, Greece", "2018", _VIPCUP, None),
    ("WIE", "4th IEEE WIECON-ECE Conference", "Thailand", "2018", _SHONGKET, "Online"),
]

_GRELY_P = "gRely: reliability estimation of variant effect predictions for genome-trained models"
_AL_P = "Evaluation of active learning selection strategies and characterization of informative sequences"

POSTERS = [
    ("CSHL", "90th Cold Spring Harbor Symposium on Quantitative Biology (AI in Biology)", "New York, United States", "2026", _GRELY_P, None),
    ("CSHL", "90th Cold Spring Harbor Symposium on Quantitative Biology (AI in Biology)", "New York, United States", "2026", _AL_P, None),
    ("CSHL", "Biological Data Science", "Cold Spring Harbor Laboratory, New York, United States", "2024", _LEAKAGE, None),
    ("ECCB", "23rd European Conference on Computational Biology", "Turku, Finland", "2024", _LEAKAGE, None),
    ("MLCB", "Machine Learning in Computational Biology", "Seattle, United States", "2024", _LEAKAGE, None),
    ("MLCB", "Machine Learning in Computational Biology", "Seattle, United States", "2023", _EVAL, None),
    ("KIP", "Kipoi Summit", "Zugspitze, Germany", "2023", _EVAL, None),
    ("CVPR", "Media Forensics Workshop, CVPR 2019", "Long Beach, United States", "2019",
     "Application of DenseNet in camera model identification and post-processing detection", None),
]

# Same shape as the talks: (mark, venue, place, when, what, note)
WORKSHOPS = [
    ("IEEE", "IEEE EMBS Region 9 Conference", "Guadalajara, Mexico", "Oct 2023",
     "Invited three-hour workshop on designing sequence-based gene regulatory deep learning models.", None),
    ("UBC", "Advanced Genomics &amp; Genome Engineering Workshop", "Michael Smith Laboratories, UBC", "Sep 2023",
     "Invited 30-minute lecture on designing sequence-based gene regulatory deep learning models.", None),
    ("SCN", "Machine Learning for Genome Editing", "Stem Cell Network, Canada", "Jun 2023",
     "Invited 90-minute workshop: using publicly available ML models for genome editing experiments, training networks on sequence-to-expression data from massively parallel reporter assays, and showing when simpler models outperform complex neural networks.", "Online"),
]


VENUE_IMG_DIR = "assets/img/venues"


def venue_mark(mark):
    """A logo if one has been added for this venue, otherwise its initials.

    Drop <mark-in-lowercase>.png (or .jpg/.svg/.webp) into assets/img/venues/
    and re-run this script; nothing else needs changing.
    """
    for ext in ("svg", "png", "webp", "jpg"):
        rel = "%s/%s.%s" % (VENUE_IMG_DIR, mark.lower(), ext)
        if os.path.exists(os.path.join(ROOT, rel)):
            return ('logo', '<img class="talkcard__logo" src="%s" alt="" '
                            'loading="lazy" decoding="async">' % rel)
    return ('initials', mark)


def render_talks(items):
    out = []
    for mark, venue, place, year, topic, note in items:
        pill = "pill--live" if note == "Upcoming" else "pill--muted"
        note_html = ('<span class="pill %s">%s</span>' % (pill, note)) if note else ""
        kind, mark_html = venue_mark(mark)
        out.append("""      <article class="talkcard">
        <span class="talkcard__mark talkcard__mark--{kind}" aria-hidden="true">{mark}</span>
        <div class="talkcard__body">
          <h3 class="talkcard__venue">{venue}</h3>
          <p class="talkcard__place">{place}</p>
          <p class="talkcard__topic">{topic}</p>
        </div>
        <p class="talkcard__when">{year}{note}</p>
      </article>""".format(kind=kind, mark=mark_html, venue=venue, place=place, topic=topic,
                           year=year, note=(" " + note_html if note_html else "")))
    return "\n".join(out)


def record(name, where=None, when=None, note=None, links=None, items=None, mark=None):
    """One row of a labelled record: what it was, where, and when.

    mark, if given, puts the same logo-or-initials tile as the talk cards in
    front of the row.
    """
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
    mark_html, cls = "", "record"
    if mark:
        kind, inner = venue_mark(mark)
        mark_html = ('\n      <span class="talkcard__mark talkcard__mark--%s record__mark" aria-hidden="true">%s</span>'
                     % (kind, inner))
        cls = "record record--marked"
    return """    <article class="{cls}">{mark}
      <div class="record__main">
{body}
      </div>{when}
    </article>""".format(cls=cls, mark=mark_html, body="\n".join(parts), when=when_html)


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
     "Which experiment would teach a model the most? In biology the question is barely asked, because the people generating data and the people modelling it are usually solving different problems. Answering it turns library design into an inference problem rather than a cataloguing exercise."),
    ("How do we train the best models?",
     "Architecture, objective, augmentation, and the dozens of small decisions in between. A published model arrives with all of them bundled together, so comparing two models rarely reveals which choice actually carried the result."),
    ("What have the models learned?",
     "A split holds nothing out when related sequences sit on both sides of it, and a model that recalls its neighbours scores like one that understands them. Telling recall apart from reasoning is a prerequisite for every claim anyone makes from a model&rsquo;s internals."),
    ("Can we trust a single prediction?",
     "An aggregate benchmark number says nothing about the case in front of you, and that is the one that matters wherever a model is actually deployed. I work on per-prediction reliability estimates, so that a model can say when it does not know."),
    ("Can we trust how we read them?",
     "Attribution and perturbation methods are instruments in their own right, and largely untested ones. A confident, accurate model read through a broken lens is worse than no model at all."),
]

TABS = [
    ("research.html", "Research", "The five questions, the projects behind them, and the funding."),
    ("publications.html", "Publications", "Journal articles, conference papers and preprints."),
    ("talks.html", "Talks", "Talks, posters and workshops I have run."),
    ("teaching.html", "Teaching", "Courses I have taught and the students I have supervised."),
    ("service.html", "Service", "Peer review, programme committees and community work."),
    ("cv.html", "CV", "The full curriculum vitae, as a PDF."),
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
        <h1>To benefit from scaling laws in biology, <em>we need to synthesize the right data with the goal of training models.</em></h1>
        <p class="hero__mission">I am a PhD candidate in Biomedical Engineering at the University of British Columbia, in the <a href="{lab}" target="_blank" rel="noopener">de Boer Lab</a>. Almost every model of gene regulation is trained on data that was generated for some other reason: an atlas, a consortium characterisation, whatever happened to get measured. The field has built remarkable models on top of leftovers, and has rarely built the experiment for the model.</p>
        <p class="hero__mission">I am working on addressing that gap. I design experiments whose purpose is to synthesize the most suitable data for training models, at a throughput worth training on.</p>
        <p class="hero__mission">Better data is only half of it. Every experiment and dataset carries its own bias, and a model will fit that bias as readily as the biology, so the rest of my work is on ensuring the models learn causal structure rather than the correlations an assay left behind, on a faithful reporting of the model&rsquo;s performance, and on knowing when to trust a prediction and the interpretation we draw from it. Trust is what makes them worth using.</p>
        <div class="hero__actions">
          <a class="btn btn--primary" href="{cv}" target="_blank" rel="noopener">Curriculum vitae (PDF)</a>
          <a class="btn btn--ghost" href="publications.html">Publications</a>
        </div>
        <p class="status">
          <span class="status__dot" aria-hidden="true"></span>
          <span><strong>I am always looking for students to work with.</strong> I have supervised six co-op and PhD students in the de Boer Lab, and motivated undergraduates and high-school students are welcome to <a href="mailto:{email}">get in touch</a>.</span>
        </p>
        <p class="hero__note">Vancouver, Canada</p>
      </div>

      <div class="hero__aside">
        <div class="portrait">
          <img src="assets/img/portrait.jpg" alt="{name}" width="720" height="720">
        </div>
        <dl class="facts">
          <div class="fact"><dt>Position</dt><dd>PhD candidate, Biomedical Engineering</dd></div>
          <div class="fact"><dt>Lab</dt><dd><a href="{lab}" target="_blank" rel="noopener">de Boer Lab</a>, School of Biomedical Engineering, UBC</dd></div>
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
          <p class="eyebrow">Topics I am interested in</p>
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
        <h2>Publications, talks and supervision.</h2>
      </div>
      <dl class="figures">
        <div class="figure"><dt>Peer-reviewed papers</dt><dd>{npeer}</dd></div>
        <div class="figure"><dt>Preprints</dt><dd>{npre}</dd></div>
        <div class="figure"><dt>Talks given</dt><dd>{ntalks}</dd></div>
        <div class="figure"><dt>Co-op and PhD students supervised</dt><dd>6</dd></div>
      </dl>
      <p class="hero__actions"><a class="btn btn--ghost" href="publications.html">All publications</a></p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Elsewhere on this site</p>
        <h2>The other pages on this site.</h2>
      </div>
      <div>
{tabs}
      </div>
    </div>
  </section>
""".format(role=ROLE, cv=CV_PDF, email=EMAIL, name=NAME, lab=LAB, themes=themes, topics=topics,
           ntopics=len(TOPICS), npeer=len(JOURNALS) + len(CONFERENCES), npre=len(PREPRINTS),
           ntalks=len(INVITED) + len(TALKS), tabs=tabs)


RESEARCH_THEMES = [
    ("How do we generate the data?",
     "Experiments built for the model, not inherited from someone else&rsquo;s",
     "A model of regulation is bounded by the sequences it was trained on. The genome supplies too few of them and they are too correlated, and synthetic libraries that lift that ceiling saturate in turn, because most of a dataset&rsquo;s value arrives early and volume alone stops buying accuracy. I have worked on random libraries that remove the homology and sample-size limits, on chromosome-scale sequence that removes fixed context, and now on designing libraries around information content rather than count."),
    ("How do we train the best models?",
     "Which design decisions actually matter",
     "A trained model is the product of dozens of choices made at once. Architecture, objective, augmentation and data handling all move the result, and a paper comparing two models cannot say which of them was responsible. Holding the data fixed and letting training vary across many independent attempts separated the factors for one setting, where it was the trainer rather than the architecture that carried the gain."),
    ("What have the models learned?",
     "Causal structure, or the shape of the training set",
     "A model that predicts well is only informative if what it learned was regulation. Homologous sequences land on both sides of a standard split, so a model that recalls its neighbours scores like one that understands them, and every assay leaves biases a model will fit as readily as the biology. I built tools that detect that homology and partition data around it, and am mapping it across the genome so the correction does not have to be recomputed each time."),
    ("Can we trust a single prediction?",
     "Reliability per prediction, not per benchmark",
     "Anyone applying these models cares about one variant, not an average. Aggregate correlations say nothing about that case, and the usual workaround of thresholding on predicted effect size discards the low-magnitude variants where most GWAS signal is expected to act. I built a meta-model that scores how far an individual prediction can be trusted, and that says which features drive the score."),
    ("Can we trust how we read them?",
     "The interpretation tools are instruments too",
     "Most biological claims from these models arrive through an interpretation method rather than from the model itself. Attribution and perturbation methods are models in their own right, far less tested than the networks they are pointed at, and a distorted lens turns an accurate model into a wrong conclusion without any benchmark catching it."),
]


# (title, status, pill class, description, [(label, url), ...])
# Unpublished entries are described by their goal only.
WORK = [
    ("hashFrag &mdash; homology, leakage and memorization", "Preprint", "pill--green",
     "Neither chromosomal nor random train/test splits account for homology within a species, so standard evaluations of genome-trained models are inflated. We measured how far, showed that the dependence on training-set similarity is not monotonic, and released hashFrag, which detects homology and partitions data at roughly a hundredth of the compute of exhaustive alignment. Its recommendation is to stratify a test set rather than build a fully orthogonal one, because an orthogonal split hides the bias instead of exposing it.",
     [("Preprint", "https://www.biorxiv.org/content/10.1101/2025.01.22.634321v2"), ("Code", "https://github.com/de-Boer-Lab/hashFrag")]),
    ("pairFrag &mdash; genome-wide homology mapping", "In preparation", "pill--live",
     "Making homology-aware evaluation something any group can do without repeating the computation.",
     []),
    ("Random Promoter DREAM Challenge", "Published", "pill--muted",
     "Random sequence removes the homology and sample-size ceilings at once. I designed and ran an open challenge on 6.7 million random promoters measured in yeast, with more than 110 teams and 28 final models; nineteen beat the previous state of the art. The winner had the fewest parameters and three of the top five used no transformer, so I built a framework that recombines the entrants&rsquo; modules across architectures and trainers to find out which choice carried the gain. It was the trainer. Models tuned on random yeast sequence then transferred to other species and assays.",
     [("Nature Biotechnology", "https://www.nature.com/articles/s41587-024-02414-w"),
      ("Code", "https://github.com/de-Boer-Lab/random-promoter-dream-challenge-2022")]),
    ("Chromosome-scale sequence from outside the host", "Ongoing", "pill--live",
     "Short oligos sit in one fixed context, so they cannot report on promoter&ndash;gene distance, chromatin or real transcripts. Sequence carried on yeast artificial chromosomes behaves like an extra chromosome and has never been under selection in the organism reading it. We annotated a single YAC in Luthra et al., then increased the data tenfold to train models on it, which became Yorzoi, built with Timon Schneider and Tom Ellis at Imperial College London. We are now scaling the data tenfold again for Yakformer.",
     [("Yorzoi preprint", "https://www.biorxiv.org/content/10.1101/2025.09.20.677345v1.abstract"),
      ("Yorzoi code", "https://github.com/Tom-Ellis-Lab/yorzoi")]),
    ("High-information-content libraries", "In progress", "pill--live",
     "Designing sequence synthesis approaches that create high-information-content sequence libraries.",
     []),
    ("nextFrag (active learning)", "Preprint", "pill--green",
     "If every sequence has to be paid for, each one should be chosen to be informative. We benchmarked six selection strategies across architectures, datasets and configurations, simulated on pools that had already been measured, so the benchmark itself needed no new experiment. All beat random sampling, uncertainty-based methods did best while being cheapest to compute, and most of the gain from many small acquisition rounds survives with fewer, larger ones &mdash; which is what makes lab-in-the-loop practical. Selected sequences look distinctive, but selecting directly on those properties never matched active learning: informativeness is a property of the model&rsquo;s ignorance, not of the sequence. Building on this, we are extending the work to large-scale experimental data, to report how active learning is best done in genomics.",
     [("Preprint", "https://www.biorxiv.org/content/10.64898/2026.05.21.727038v1"), ("Code", "https://github.com/de-Boer-Lab/nextFrag")]),
    ("gRely &mdash; reliability of individual predictions", "Preprint", "pill--green",
     "A meta-model that estimates the probability an individual variant-effect prediction is correct, from features of the variant, gene, tissue and model. Its top-scoring fifth reaches 97% sign concordance against 54% in the bottom fifth, and it stays discriminative among the low-magnitude variants that effect-size filtering discards, which is where most GWAS signal is expected to act. It transfers zero-shot to other architectures, so reliability looks like a property of the locus rather than of the model. Begun during an internship at Genentech.",
     [("Preprint", "https://www.biorxiv.org/content/10.64898/2026.05.23.727431v1")]),
]


# (title, when, source, PI, funding, role)
PROJECTS = [
    ("Four Year Doctoral Fellowship (4YF)", "2021 &ndash; 2025",
     "University of British Columbia", None,
     "96,000 CAD over four years",
     "UBC&rsquo;s flagship doctoral fellowship, awarded with tuition to top PhD students"),
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
    for title, status, pill, text, links in items:
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
          <p class="project__text">{text}</p>{links}
        </article>""".format(title=title, pill=pill, status=status, text=text, links=link_html))
    return "\n".join(out)


def research():
    themes = "\n".join(
        record(title, where=sub, note=body) for title, sub, body in RESEARCH_THEMES)
    projects = "\n".join(
        record(t, where=("%s &middot; PI: %s" % (s, p)) if p else s,
               when=w, note="%s. %s." % (f, r))
        for t, w, s, p, f, r in PROJECTS)

    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Research</p>
        <h1>Learning the cis-regulatory code from sequence.</h1>
        <p class="lede">How do we learn the cis-regulatory code from sequence, and how do we know when to trust what a model has learned?</p>
      </div>
      <div class="prose prose--wide">
        <p>Progress on cis-regulation is limited by <strong>data rather than architecture</strong>. The genome offers too few examples, they are too correlated with one another, and its homology structure makes standard evaluations dishonest. Almost all of that data was also generated for a different purpose: characterising a system and training a model on it are different objectives, and technology built deliberately to produce training data is rare.</p>
        <p>So the work runs in two directions at once. One builds the data, using synthetic sequence to escape the genome&rsquo;s ceilings and designing it for information content rather than count. The other keeps the resulting models honest: evaluated without leakage, reported faithfully, and able to say how far an individual prediction can be trusted.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Themes</p>
        <h2>The questions the work is organised around.</h2>
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
        <h2>Projects, published and in progress.</h2>
      </div>
      <div class="projects">
{work}
      </div>
      <p class="status status--wide">
        <span class="status__dot" aria-hidden="true"></span>
        <span>Interested in collaborating on any of these? <a href="mailto:{email}" aria-label="Email me" title="Email me">Reach out {mail}</a>.</span>
      </p>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Funding</p>
        <h2>Grants and compute.</h2>
        <p class="lede">Fellowships, grants and compute awards, with the role I held on each.</p>
      </div>
      <div class="records">
{projects}
      </div>
    </div>
  </section>
""".format(themes=themes, work=render_work(WORK), projects=projects,
           email=EMAIL, mail=icon("mail", "inlineicon"))


def publications():
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Publications</p>
        <h1>Publications and preprints.</h1>
        <p class="lede">Also on <a href="{scholar}" target="_blank" rel="noopener">Google Scholar</a>.</p>
      </div>
      <dl class="figures">
        <div class="figure"><dt>Journal articles</dt><dd>{njournal}</dd></div>
        <div class="figure"><dt>Conference papers</dt><dd>{nconf}</dd></div>
        <div class="figure"><dt>Preprints</dt><dd>{npre}</dd></div>
      </dl>

      <div class="pubs">
        <div class="grouplabel"><p class="eyebrow">Preprints</p><span class="fieldindex__count">{npre} entries</span></div>
{preprints}
        <div class="grouplabel"><p class="eyebrow">Journal articles</p><span class="fieldindex__count">{njournal} entries</span></div>
{journals}
        <div class="grouplabel"><p class="eyebrow">Conference papers</p><span class="fieldindex__count">{nconf} entries</span></div>
{conferences}
      </div>
      <p class="legend"><sup>*</sup> Equal contribution &nbsp;&middot;&nbsp; <sup>&dagger;</sup> Corresponding author</p>
    </div>
  </section>
""".format(scholar=SCHOLAR,
           npre=len(PREPRINTS), njournal=len(JOURNALS), nconf=len(CONFERENCES),
           preprints=render_pubs(PREPRINTS), journals=render_pubs(JOURNALS),
           conferences=render_pubs(CONFERENCES))


def talks():
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Talks</p>
        <h1>Talks, posters and workshops.</h1>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Invited</p>
        <h2>Invited talks.</h2>
      </div>
      <div class="talks">
{invited}
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Contributed</p>
        <h2>Conference and meeting talks.</h2>
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
      <div class="talks">
{workshops}
      </div>
    </div>
  </section>
""".format(invited=render_talks(INVITED), talks=render_talks(TALKS),
           posters=render_talks(POSTERS), workshops=render_talks(WORKSHOPS))


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
               where="University of British Columbia", when="Sep 2021 &ndash; Dec 2024", mark="UBC",
               note="Eleven courses across the MDS curriculum, from supervised learning and regression through workflows, visualisation and cloud computing.",
               items=[i[4:-5] for i in mds_items]),
        record('Graduate Teaching Assistant &mdash; <a href="https://www.biology.ubc.ca/" target="_blank" rel="noopener">Biology Program</a>',
               where="University of British Columbia", when="May &ndash; Jun 2022", mark="UBC",
               items=["BIOL 234: Fundamentals of Genetics"]),
        record('Graduate Teaching Assistant &mdash; <a href="https://www.uwindsor.ca/engineering/electrical/" target="_blank" rel="noopener">Electrical and Computer Engineering</a>',
               where="University of Windsor", when="Jan &ndash; Dec 2020", mark="UW",
               items=["ELEC 8330: Computational Intelligence", "GENG 2320: Engineering Software Fundamentals"]),
    ])

    mentorship = "\n".join([
        record('<a href="https://bsri-bd.github.io/" target="_blank" rel="noopener">Bangladeshi Student Research Initiative</a>',
               where="Founder", when="2024 &ndash; present", mark="BSRI",
               note="A non-profit connecting undergraduate and postgraduate students in Bangladesh with Bangladeshi researchers in academia and industry abroad, through free mentorship programmes. Mentees are matched across a volunteer network, so the students I mentor through it are separate from those I supervise in the lab."),
        record('<a href="%s" target="_blank" rel="noopener">de Boer Lab</a>' % LAB,
               where="School of Biomedical Engineering, UBC", when="2023 &ndash; present", mark="DBL",
               note="Sole supervisor for five co-op students on self-designed research projects; one of them went on to receive SBME Synergy funding. I also mentor PhD students in the lab."),
    ])

    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Teaching</p>
        <h1>Teaching and supervision.</h1>
        <p class="lede">Courses I have taught as a graduate teaching assistant, and the co-op and PhD students I have supervised.</p>
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
        <h2>Courses I have taught.</h2>
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
        <h2>Students I have supervised.</h2>
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
    ("BSc thesis committee member",
     "Faculty of Science, University of British Columbia", "2025", None),
]


COMMUNITY = [
    ("Organising committee, Bangladeshi Student Research Initiative",
     "Volunteer research network connecting students in Bangladesh with researchers abroad", "2024 &ndash; present",
     None),
    ("President, Bangladeshi Grad Alliance UBC", "University of British Columbia", "2024 &ndash; 2025",
     "Co-founded the organisation and served as its inaugural President, establishing the first executive committee and running community events for Bangladeshi graduate students."),
    ("Project manager, SynBio 6.0", "University of British Columbia", "2024",
     "Managed the organisation of a two-day national synthetic biology symposium hosted at UBC, bringing together around 100 Canadian researchers."),
    ("Project co-ordinator and organiser, Random Promoter DREAM Challenge", "UBC, IBM Research and Sage Bionetworks", "2022",
     "Co-organised an international competition with over 100 teams &mdash; roughly 300 scientists from 75+ universities and companies &mdash; to build models predicting gene expression from sequence. Ran daily operations as the only graduate student on the organising committee."),
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
        <h2>Committee service.</h2>
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
        <h2>Events and organisations.</h2>
      </div>
      <div class="records">
{community}
      </div>
    </div>
  </section>

""".format(independent=reflist(REVIEW_INDEPENDENT), co=reflist(REVIEW_CO),
           roles=roles, community=community)


def cv():
    return """
<section class="section section--plain">
    <div class="wrap">
      <div class="section__head">
        <p class="eyebrow">Curriculum vitae</p>
        <h1>The full CV, as a PDF.</h1>
        <p class="lede">Education, positions, funding and awards are all in the document below. Publications, talks, teaching and service each have their own page on this site.</p>
      </div>
      <div class="downloads">
        <a class="download" href="{cv}" target="_blank" rel="noopener">
          <span class="download__name">Curriculum vitae</span>
          <span class="download__text">Education, research and work experience, publications, talks, posters, funding, service and awards.</span>
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
""".format(cv=CV_PDF, failure=FAILURE_PDF)


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
     "Talks, selected posters and workshops given by Abdul Muntakim Rafi.",
     talks),
    ("teaching.html", "Teaching",
     "Courses taught at UBC and the University of Windsor, and students supervised in the de Boer Lab and beyond.",
     teaching),
    ("service.html", "Service",
     "Peer review, programme committees, memberships and community organising.",
     service),
    ("cv.html", "CV",
     "The full curriculum vitae of Abdul Muntakim Rafi, as a downloadable PDF.",
     cv),
]


def main():
    for slug, title, desc, builder in PAGES:
        path = write(slug, title, desc, builder())
        print("wrote %s" % os.path.relpath(path, ROOT))


if __name__ == "__main__":
    main()
