"""Research section for graybearstudio.com: the Hidden Structure Research Group.

Builds /research/ and five sub-pages. Self-contained: build.py imports this module
and calls build_research(page, write, href, DIST, ROOT) once. Figures are inlined SVG
(they read the page's CSS colour variables, so they follow light and dark mode).
Maths is converted to MathML at build time with latex2mathml (pip install latex2mathml),
so pages load no extra scripts and make no third-party requests.

Public-copy rules honoured: no em dashes; no personal name, rank, unit or service.
"""
import html
import os
import shutil

from latex2mathml.converter import convert as _tex

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
SECTION = {
    "slug": "research",
    "name": "Research",
    "accent": ("#2F6F68", "#7FD1C1"),   # visible: aurora teal
    "accent2": ("#6A4F8F", "#B9A3E3"),  # hidden: violet
    "pages": False,
    "footer_notes": ["Research notes from the Hidden Structure Research Group, a project of GrayBear Studio. "
                     "Mathematics, not medical, financial or professional advice."],
}

PAGES = [
    ("research", "Overview"),
    ("research/idea", "The idea"),
    ("research/results", "What is proved"),
    ("research/open", "Open questions"),
    ("research/predictions", "Predictions and papers"),
    ("research/corrections", "Corrections"),
]


# ------------------------------------------------------------------ helpers
def m(tex):
    """inline maths"""
    return _tex(tex)


def eq(tex, note=""):
    n = f'<span class="rs-eqnote">{note}</span>' if note else ""
    return f'<div class="rs-eq">{_tex(tex, display="block")}{n}</div>'


def fig(name, caption, wide=True):
    with open(os.path.join(HERE, "figures", name + ".svg"), encoding="utf-8") as f:
        s = f.read()
    cls = "rs-figure wide" if wide else "rs-figure"
    return f'<figure class="{cls}">{s}<figcaption>{caption}</figcaption></figure>'


LABELS = {
    "proved": "Proved",
    "model": "Proved in a model",
    "numerical": "Numerical evidence",
    "open": "Open",
    "interp": "Interpretation",
}


def label(k):
    return f'<span class="rs-label {k}">{LABELS[k]}</span>'


def subnav(href, here):
    links = []
    for path, name in PAGES:
        cur = ' aria-current="page"' if path == here else ""
        links.append(f'<a href="{href(here, path)}"{cur}>{E(name)}</a>')
    return f'<nav class="rs-subnav" aria-label="Research sections"><div class="wrap">{"".join(links)}</div></nav>'


# pre-rendered maths (kept out of f-strings for Python < 3.12)
_T1 = eq(r"p(x)=2^{-m}\sum_{S\subseteq\{1,\dots,m\}}\hat{p}(S)\,\chi_S(x),\qquad \chi_S(x)=(-1)^{\sum_{i\in S}x_i}",
    "Each group of switches S gets one number, its coefficient. The size of S is the size of the pattern.")
_T2 = eq(r"A_t=\{S: |S|\le t\},\qquad \ker\Phi_t=\operatorname{span}\{\chi_S: |S|>t\}",
    "What a depth-t observer can see, and the hidden kernel: everything it can never see. This is the Observer-Kernel Theorem.")
_T3 = eq(r"p(x_1,x_2,x_3)=\begin{cases}\tfrac14 & x_1\oplus x_2\oplus x_3=0\\ 0 & \text{otherwise}\end{cases}",
    "Every coefficient of size one and two is zero, while the size-three coefficient is not. This is the minimal example of non-reconstructibility.")
_T4 = eq(r"\mathrm{SHOM}_t(p)=\sum_{|S|>t}\hat{p}(S)^2")
_T5 = eq(r"\frac{D_t}{2^m}=\Pr\!\left[\mathrm{Bin}\!\left(m,\tfrac12\right)>t\right]",
    "The Walsh Threshold Theorem. As m grows, this drops from nearly 1 to nearly 0 at t/m = 1/2, over a window of width about 1/√m.")
_T6 = eq(r"I_t\subsetneq I_{t+1},\qquad \ker\Phi_{\mathrm{fus}}=\operatorname{span}\{\chi_S: S\notin F_{\mathrm{fus}}\}",
    "The Strict Observer Hierarchy and the Observer Fusion Theorem.")
_T7 = eq(r"P_0\,p=p_u=2^{-m}\ \text{for every }p",
    "The Dephasing Convergence Theorem and Unity Non-Recovery.")
_T8 = eq(r"\Phi=\Lambda\circ\Delta\circ U,\qquad \Delta(U\,c\,U^\dagger)=0\ \text{for every coherence }c",
    "The Interface Structure Theorem and Coherence Invisibility. Rearrange, then erase, then post-process.")
_T9 = eq(r"[Z_U, X_U]=0\iff |U|\ \text{is even}", "The Parity Rule. Standard quantum algebra, restated in the program's language.")
_T10 = eq(r"\tau_{AB}+\tau_{BC}+\tau_{CA}=0")
_T11 = eq(r"\text{local hidden state: } S\le2,\qquad \text{quantum pairs: } S=2\sqrt2", "The CHSH bound. A known result, used here to locate the open question.")
_T12 = m(r"1/\sqrt{m}")


# ------------------------------------------------------------------ page bodies
def body_overview(href):
    h = "research"
    return f"""
<section class="rs-hero"><div class="wrap">
<div>
<p class="eyebrow">Hidden Structure Research Group</p>
<h1>What can an observer never see?</h1>
<p class="tag">A mathematics program about the limits of observation.</p>
<p class="lede">Every observer, whether a person, an animal, an instrument or a machine, sees the world through a filter
that can only compare a few things at once. The Observer Limit Program asks what that filter hides for good,
proves exactly where the edge lies, and tests what the hidden part does.</p>
</div>
<div>{fig("filter", "Six switches have 64 possible patterns, sorted here by size. An observer that compares at most two "
                    "things at a time sees the 22 patterns below the line. The 42 above it are not faint or blurry to it. "
                    "They are invisible.", wide=False)}</div>
</div></section>
{subnav(href, h)}
<section class="section"><div class="wrap">
<h2>Three ideas</h2>
<div class="rs-ideas">
<div class="rs-idea"><div class="k">01</div><h3>Patterns come in sizes</h3>
<p>Any pattern across many yes-or-no switches splits cleanly into pieces: single switches, pairs, triples, and so on,
up to the whole system at once. Nothing is left over.</p></div>
<div class="rs-idea"><div class="k">02</div><h3>Every observer has a depth</h3>
<p>An observer that can compare at most a few things at a time sees the small pieces exactly and is blind to the large
ones. More data does not help. Only a deeper observer can see them.</p></div>
<div class="rs-idea"><div class="k">03</div><h3>The edge is sharp</h3>
<p>For a large system, an observer whose depth is below half the system misses almost everything. Above half, almost
nothing is hidden. The switch from one to the other gets sharper as systems grow.</p></div>
</div>
</div></section>
<section class="section"><div class="wrap col">
<div class="rs-box">
<h2>How sure are we?</h2>
<p>Every result on these pages carries one of five labels, and the labels are not decoration. Proved means proved
within the stated mathematical setup, which is a claim about mathematics, not about the physical world.</p>
<ul class="rs-legend">
<li><span>{label("proved")}</span><span>A complete proof exists for the stated setup.</span></li>
<li><span>{label("model")}</span><span>Exact, but inside a specific model that the program chose and has not yet derived.</span></li>
<li><span>{label("numerical")}</span><span>Strong computational evidence. Not a theorem.</span></li>
<li><span>{label("open")}</span><span>Unresolved. Stated so that it can be settled.</span></li>
<li><span>{label("interp")}</span><span>What a result might mean. Never offered as evidence.</span></li>
</ul>
<p style="margin-top:1.2rem">Predictions about a computation are sealed before it is run. Since September 2026, every
computed number is logged with a fingerprint of the script that produced it. When something turns out to be wrong, the
correction is published, not buried.</p>
</div>
</div></section>
<section class="section"><div class="wrap">
<h2>Explore</h2>
<div class="rs-nav">
<a href="{href(h, 'research/idea')}"><b>The idea, step by step</b><span>Plain language first, then the formula, with pictures.</span></a>
<a href="{href(h, 'research/results')}"><b>What is proved</b><span>The main theorems and the walls the program has hit.</span></a>
<a href="{href(h, 'research/open')}"><b>Open questions</b><span>What is not settled, and what would settle it.</span></a>
<a href="{href(h, 'research/predictions')}"><b>Predictions and papers</b><span>Where the mathematics meets experiment.</span></a>
<a href="{href(h, 'research/corrections')}"><b>Corrections</b><span>What we said, what is true now, and why it changed.</span></a>
</div>
</div></section>"""


def body_idea(href):
    h = "research/idea"
    return f"""{subnav(href, h)}
<article class="rs-doc"><div class="wrap col">
<h1>The idea, step by step</h1>
<p class="sub">Plain language first, then the mathematics</p>
<p class="lead">This page builds the central idea from nothing. Each step says it in words, then shows the formula
behind it. You can skip every formula and still follow the story.</p>

<h2><span class="n">STEP 1</span>Patterns come in sizes</h2>
<p>Picture {m("m")} switches, each on or off. A situation is one setting of all of them. Some patterns involve one
switch ("switch 3 is usually on"). Some involve a pair ("switches 2 and 5 tend to agree"). Some involve three, or
four, or all of them at once.</p>
<p>A classical result from mathematics, the Walsh or Fourier decomposition, says that any way of assigning chances to
the situations splits exactly into pieces of these sizes, one piece for every group of switches. With {m("m")}
switches there are {m("2^m")} groups, so {m("2^m")} pieces, and together they rebuild the whole thing perfectly.</p>
{_T1}

<h2><span class="n">STEP 2</span>An observer is a filter</h2>
<p class="rs-plain">An observer that can compare at most {m("t")} things at a time sees every pattern of size {m("t")}
or less, exactly, and nothing larger.</p>
<p>This is what depth means here. A depth-two observer can measure every single switch and every pair. It cannot
measure any triple. The larger patterns are not faint to it. They are absent from everything it can record.</p>
{_T2}
{fig("filter", "The same picture as the overview: 64 patterns of six switches, sorted by size. Teal is what a "
               "depth-two observer sees. Violet is the hidden kernel above the line.")}

<h2><span class="n">STEP 3</span>The smallest hidden pattern: three coins</h2>
<p>Here is a pattern no shallow observer can ever detect. Toss three coins with one hidden rule: the number of heads is
always even. Look at any one coin: heads half the time. Look at any two: all four outcomes, equally often. Every
measurement of one or two coins says "pure chance."</p>
<p>Look at all three together and the rule is obvious: half of the possible patterns never happen. The structure exists
only at the level of the whole.</p>
{fig("coins", "Every pair of coins looks completely random. Only the three together reveal the rule.")}
{_T3}
<p>The program measures how much structure sits out of reach with one number, the hidden higher-order mass:</p>
{_T4}

<h2><span class="n">STEP 4</span>The edge is sharp</h2>
<p>How much is hidden? Count the pieces. Of the {m("2^m")} pieces, those larger than {m("t")} are hidden. The share of
hidden pieces turns out to be a coin-flip probability: the chance that {m("m")} fair coins show more than {m("t")}
heads.</p>
{_T5}
{fig("threshold", "The hidden share against observer depth, for systems of 8, 32 and 256 switches. Bigger systems switch "
                  "more sharply at one half.")}
<p>So a large system has a built-in horizon. An observer below half its size sees almost none of its structure. Exactly
at half, an observer stays balanced, with almost exactly half visible, however large the system becomes.</p>

<h2><span class="n">STEP 5</span>Deeper observers, and many observers</h2>
<p>Depth makes a strict ladder: for every depth there is structure that is invisible one step down and visible one
step up. And observers can pool what they see. Two observers with different windows, combined, see the union of their
windows, and a family that covers every pattern sees everything a classical observer could.</p>
{_T6}

<h2><span class="n">STEP 6</span>Return to the ground</h2>
<p>Now run the filter as a process. Erase the largest patterns, then the next largest, and so on. What remains at the end
is the uniform state, where every situation is equally likely and nothing can be told apart. The program calls it
unity. From unity there is no way back: every starting point ends there, so the end cannot tell you where you began.</p>
{fig("ground", "Each step removes the largest remaining patterns. The last step leaves only unity.")}
{_T7}

<h2><span class="n">STEP 7</span>The quantum version</h2>
<p>The same picture carries over to quantum systems, where the patterns become products of the Pauli matrices
{m("X, Y, Z")}. The accessible data are the {m("Z")}-type patterns. The {m("X")} and {m("Y")} types form a hidden
coherent sector, and the program proves that the standard kind of measurement interface erases it completely.</p>
{_T8}
<p>One consequence is easy to state. Looking at a hidden pattern always costs something visible: a look at a set
{m("U")} of sites wipes out exactly the visible patterns that overlap {m("U")} an odd number of times. A single
particle is always the odd case, which is the familiar fact that measuring spin one way scrambles it the other way.
For a pair, both can be known at once.</p>
{_T9}

<h2><span class="n">INTERPRETATION</span>What it might mean</h2>
<p>{label("interp")}</p>
<p>The mathematics says that every bounded observer has a permanent hidden side, one that is not empty, only out of reach,
and that some facts exist only at the level of the whole. Whether that says anything about minds, or about what lies
beyond a single point of view, is a question the mathematics can sharpen but cannot settle. It is offered here as a
question, not as a result.</p>
</div></article>"""


# (label, number, title, plain sentence, latex, note)
RESULTS = [
    ("The wall", "What a bounded observer can never reconstruct.", [
        ("proved", 1, "Walsh Threshold Theorem",
         "The share of structure hidden from a depth-t observer is a coin-flip probability, and it switches sharply at half the system size.",
         r"\frac{D_t}{2^m}=\Pr\!\left[\mathrm{Bin}(m,\tfrac12)>t\right]", "Transition width shrinks like 1/√m."),
        ("proved", 2, "Observer-Kernel Theorem",
         "What a depth-t observer can never see is exactly the patterns larger than t. Different worlds can look identical to it.",
         r"\ker\Phi_t=\operatorname{span}\{\chi_S:|S|>t\}", ""),
        ("proved", 3, "Irreducible Higher-Order Structure",
         "For every size above an observer's depth there are two worlds that agree on everything it sees and differ in a pattern of that size.",
         r"\Pi_{\le t}\,p_+=\Pi_{\le t}\,p_-,\qquad \hat p_\pm(S)=\pm\varepsilon", ""),
        ("proved", 4, "Strict Observer Hierarchy",
         "Each step of depth reveals structure that the step below cannot encode.",
         r"I_t\subsetneq I_{t+1}\quad\text{for every }t<m", ""),
        ("proved", 6, "Non-Reconstructibility, local form",
         "If any structure lies above pairs, no collection of pairwise views can rebuild it. Three coins with an even-count rule is the smallest example.",
         r"\mathrm{SHOM}_2(p)>0\implies \exists S,\ |S|\ge3,\ \hat p(S)\neq0", "The broad cross-field version is a proposed principle; this local statement is the proved core."),
        ("proved", 5, "Projective Extremizer Theorem",
         "The most hidden pattern that still looks flat to every pairwise view is not chaos. It is the most symmetric object available, a projective geometry over the two-element field.",
         r"m=2^k-1:\ \text{extremizer uniform on a simplex-code coset, i.e. } \mathrm{PG}(k-1,2)", ""),
    ]),
    ("The boundary", "What happens at the edge of what can be seen.", [
        ("proved", 7, "Permanent Midpoint Theorem",
         "An observer at exactly half the system size stays balanced between visible and hidden, however large the system grows.",
         r"\frac{|A_{m/2}|}{2^m}=\frac12+\frac{1}{2}\binom{m}{m/2}2^{-m}\ \longrightarrow\ \frac12", ""),
        ("proved", 10, "Finite Symmetry Obstruction",
         "No finite set of directions can have the full rotational symmetry of a sphere. Smooth space needs more than a finite compass.",
         r"X\subset S^2\ \text{finite}\implies \mathrm{Sym}(X)\neq SO(3)", ""),
        ("proved", 11, "No Spontaneous Selection",
         "Perfectly identical observers do not arrange themselves into a geometry on their own. Some extra relation has to break the symmetry.",
         r"T\ \text{equivariant},\ a^*\ \text{unique}\implies \pi a^*=a^*\ \ \forall\pi\in S_m", ""),
        ("proved", 12, "Extended Scale No-Go",
         "The observer algebra fixes shapes and ratios but not absolute size. One physical ruler has to come from outside.",
         r"\ell\to\alpha\ell,\ G\to\alpha^2G\ \text{leaves the algebra unchanged}", ""),
    ]),
    ("Many observers", "Combining, erasing and returning to the ground.", [
        ("proved", 17, "Observer Fusion Theorem",
         "Observers with different windows can pool them. A family that covers every pattern sees everything.",
         r"\ker\Phi_{\mathrm{fus}}=\operatorname{span}\{\chi_S:S\notin F_{\mathrm{fus}}\}", ""),
        ("proved", 19, "Dephasing Convergence Theorem",
         "Erasing structure shell by shell always ends at unity, where nothing can be told apart.",
         r"P_0\,p=p_u\ \ \text{for every } p", ""),
        ("proved", 14, "Unity Non-Recovery",
         "Many different worlds erase to the same blank state, so the blank state cannot tell you which one you started from.",
         r"R\circ P_0=\mathrm{id}\ \text{is impossible}", ""),
    ]),
    ("The quantum interface", "What survives a measurement, and what does not.", [
        ("proved", 39, "Interface Structure Theorem",
         "Every complete interface in the program does three things in order: rearranges, erases the quantum coherence, then processes what is left classically.",
         r"\Phi=\Lambda\circ\Delta\circ U", ""),
        ("proved", 42, "Interface Rendering No-Go",
         "Inside that interface class, hidden quantum structure can never become visible data. A doorway that renders it would have to be a new kind of structure.",
         r"\Pi_D\,(U\,c\,U^\dagger)=0\ \ \text{for every coherence } c", ""),
        ("proved", 43, "Unital-Drive No-Go",
         "Under the program's own erasure process, no amount of shaking can keep a structured quantum state alive. Everything settles to the blank state.",
         r"\mathrm{Re}\,\mathrm{Tr}[\rho\,\mathcal L(\rho)]\le0\implies \rho^*=I/16", ""),
        ("proved", 45, "Holographic boundary identity",
         "For symmetric four-site states, sitting on the boundary of the holographic entropy cone is exactly the same as having one entropy constant for every cut.",
         r"I_3=12\,[\,c_W(4,1)-c_W(4,2)\,]", ""),
        ("model", 47, "The tetrahedral-angle root",
         "Requiring two neighbouring depths to agree picks out the angle whose cosine is minus one third, the tetrahedral angle, without putting it in by hand. At that angle no single site carries coherence of its own.",
         r"\cos\alpha=-\tfrac13", "This is four-switch counting, not independent evidence for geometry."),
    ]),
    ("Toward spacetime", "What the algebra gives, and where it stops.", [
        ("proved", 28, "Observer metric signature",
         "The observer's filter splits directions into one kept and others discarded, which gives the plus, minus, minus, minus sign pattern of spacetime, algebraically.",
         r"g_{\mathrm{obs}}(A,B)=\langle A,(2\Pi_D-I)B\rangle_{\mathrm{HS}}", "Algebraic only. It does not by itself establish physical Lorentz symmetry."),
        ("proved", 31, "Fixed-Depth Causal-Set No-Go",
         "Counting what a depth-four observer can reach grows like the fourth power, but the causal structure stays four steps tall, so it is not four-dimensional spacetime.",
         r"f_t\sim\frac{2(2^t-1)\,t!}{r^t}\to0,\qquad H=t", "A correction to an earlier reading; see Corrections."),
        ("proved", 36, "Scalar-Kernel No-Locking",
         "A single scalar coupling between observers cannot lock their internal directions to directions in space. A real link needs tensor structure.",
         r"F_{ij}=P[\partial_iP,\partial_jP]P=0", ""),
    ]),
]


def body_results(href):
    h = "research/results"
    groups = []
    for title, sub, items in RESULTS:
        cards = []
        for lab, num, name, plain, tex, note in items:
            nt = f'<p class="note">{E(note)}</p>' if note else ""
            cards.append(f'<div class="rs-result"><div class="top">{label(lab)}<span class="num">No. {num}</span></div>'
                         f'<h3>{E(name)}</h3><p>{E(plain)}</p><div class="eq">{_tex(tex, display="block")}</div>{nt}</div>')
        groups.append(f'<section class="rs-group"><h2>{E(title)}</h2><p>{E(sub)}</p><div class="rs-results">{"".join(cards)}</div></section>')
    return f"""{subnav(href, h)}
<article class="rs-doc"><div class="wrap col">
<h1>What is proved</h1>
<p class="sub">Selected results, with their labels</p>
<p class="lead">A selection of the program's results, each in one plain sentence and one formula. The walls matter as much
as the theorems: a no-go result tells you exactly where a route ends, so nobody has to walk it again.</p>
<p>Proved means proved within the stated mathematical setup. None of these is a claim that the physical world works this
way. Numbers refer to the program's full theorem index.</p>
{"".join(groups)}
</div></article>"""


def body_open(href):
    h = "research/open"
    return f"""{subnav(href, h)}
<article class="rs-doc"><div class="wrap col">
<h1>Open questions</h1>
<p class="sub">What is not settled, and what would settle it</p>
<p class="lead">The program's main results are walls as well as theorems, and the walls point at the questions that
matter. These are the ones currently open, stated so that each could be settled.</p>

<h2>The story so far</h2>
<ol class="rs-map">
<li><b>Patterns split by size</b><span>Any pattern across switches is a sum of pieces, one per group.</span></li>
<li><b>Depth fixes what is visible</b><span>A depth-t observer sees exactly the pieces of size t or less.</span></li>
<li><b>More depth, or more observers, sees more</b><span>A strict ladder, and windows that can be pooled.</span></li>
<li><b>Measurement erases the quantum side</b><span>The interface keeps the visible part and deletes coherence.</span><span class="wall">Wall: hidden structure cannot become visible inside this interface.</span></li>
<li><b>Filtering gives a sign pattern</b><span>One kept direction, the rest discarded: plus, minus, minus, minus.</span><span class="wall">Wall: algebra alone is not physical spacetime.</span></li>
<li><b>Many cells give a geometry</b><span>Coupled cells have long-wavelength modes with a natural notion of distance.</span><span class="wall">Wall: positive couplings spread like ink, not like light.</span></li>
<li class="open"><b>Which quantum state is selected?</b><span>The classical rules fix the visible part but not the quantum interior.</span></li>
</ol>

<div class="rs-open">{label("open")}
<h3>Which quantum interior does nature pick?</h3>
<p>The program's classical rules fix what an observer sees on average, but many different quantum states agree with
those rules. Something else must choose among them.</p>
<dl>
<dt>Known</dt><dd>The usual candidates fail in exact ways: shaking the system, symmetry, and agreement on visible data alone
all fail to choose. {label("numerical")} Requiring neighbouring observers to stay consistent strongly favours two-way couplings.</dd>
<dt>Would settle it</dt><dd>A proof that consistency forces the coupling to be two-way, and a principle that picks which
two-way coupling.</dd>
</dl></div>

<div class="rs-open">{label("open")}
<h3>Can what is hidden for one observer be visible to another?</h3>
<p>Inside the program's measurement interface, provably not. A doorway between observers would need a new kind of
structure, and it has to be derived rather than assumed.</p>
<dl>
<dt>Known</dt><dd>The interface no-go, and a symmetry argument showing that relabelling every observer the same way
changes nothing.</dd>
<dt>Would settle it</dt><dd>A derived rule for how neighbouring observers' frames connect, with something measurable when
you go around a loop.</dd>
</dl></div>

<div class="rs-open">{label("open")}
<h3>Does spacetime emerge from observers?</h3>
<p>The algebra produces the right sign pattern and a Lorentz-type algebra, but every dynamics tested so far fails to turn
these into physical motion through space.</p>
<dl>
<dt>Known</dt><dd>Several precise no-go results: fixed-depth counting is not four-dimensional causal structure; single
scalar couplings cannot lock internal directions to space; a light cone appears only when a coupling is tuned by hand.</dd>
<dt>Would settle it</dt><dd>A rule, derived from the observer axioms, for how cells glue together into a large-scale,
direction-free whole.</dd>
</dl></div>

<div class="rs-open">{label("open")}
<h3>Can observers share one clock?</h3>
<p>Three observers share a single time only if going around the loop between them leaves no leftover lag. The criterion is
proved; the program does not yet have a correlated three-observer state to test it on.</p>
{_T10}
</div>

<div class="rs-open">{label("open")}
<h3>What do correlations of the whole add?</h3>
<p>A rule that observers can never know more than half of a hidden state reproduces much of quantum behaviour, but no rule
of that kind can reach the correlations seen in entangled pairs. Whether the program's whole-only structure accounts for
the difference is a question, not a result.</p>
{_T11}
</div>
</div></article>"""


def body_predictions(href):
    h = "research/predictions"
    return f"""{subnav(href, h)}
<article class="rs-doc"><div class="wrap col">
<h1>Predictions and papers</h1>
<p class="sub">Where the mathematics meets experiment</p>
<p class="lead">A theory of observer limits should say something testable about real observers. The program makes three
predictions that come from the threshold theorem. Each is stated in advance, so that data can confirm or refute it.</p>

<h2><span class="n">PREDICTION 1</span>A threshold in perception</h2>
<p>If awareness depends on integrating patterns up to some depth, then for stimuli built from Walsh patterns, the point
where people stop detecting structure should sit at a predictable fraction of the stimulus size, and the transition
should get narrower as stimuli grow, roughly like {_T12}.</p>
<p>Status: a preregistered protocol is written. No results yet.</p>

<h2><span class="n">PREDICTION 2</span>Neural population codes</h2>
<p>In recordings from populations of neurons responding to Walsh-structured stimuli, the share of information carried by
high-order patterns should show a compressed transition near depth one half, with the same width scaling.</p>
<p>Status: a manuscript describes the analysis. No results yet.</p>

<h2><span class="n">PREDICTION 3</span>Learning in neural networks</h2>
<p>When an artificial network suddenly learns a rule after a long plateau, the abruptness of that jump should scale with
network width the way the threshold theorem predicts for order-limited access.</p>
<p>Status: a manuscript describes the prediction. No results yet.</p>

<h2>Papers and archive</h2>
<p>The program's papers, proofs and data are being prepared for this page. Each will be listed with its status, and every
computational result will link to the script that produced it.</p>
</div></article>"""


CORRECTIONS = [
    ("September 2026", "The depth-four count",
     "A depth-four observer's reachable region grows like the fourth power, which explains four-dimensional spacetime volume.",
     "The count is correct, but the causal structure inside it is only four steps tall and its ordering fraction goes to zero. "
     "That is the opposite of four-dimensional spacetime. The identity stands as a counting result only."),
    ("September 2026", "Clocks from observation",
     "Bounded observation forces a clock with a proper time direction.",
     "No finite system can carry an exact clock of that kind, and the blank state has no time at all. "
     "What survives: any structured state carries a modular flow, which is weaker."),
    ("September 2026", "Visible dynamics and light cones",
     "Any dynamics that only touches visible data must spread diffusively, so no light cone can come from it.",
     "False in general: a classical shift process touches only visible data and still has a strict cone. "
     "The no-go holds only for the program's positive scalar couplings."),
    ("September 2026", "A missing signature",
     "Three coupled pairs have the wrong signature for spacetime.",
     "A symplectic form has no signature. The correct statement is narrower: three pairs carry no vector of boost generators, "
     "and a fourth pair is the minimal repair."),
    ("September 2026", "Phase as an axiom",
     "A quantum state must carry complex phases to be the right state.",
     "The test was coordinate-dependent: a simple relabelling makes the state real without changing anything physical. "
     "It was replaced by a test that does not depend on coordinates."),
    ("September 2026", "A driven quantum cell",
     "A driven cell settles into a structured, holographically compatible state.",
     "The model used to show this was not a legitimate quantum process. The result was withdrawn and later replaced by a "
     "legitimate construction with a weaker conclusion."),
    ("September 2026", "Exact solutions at first order",
     "Exact consistent states exist at leading order.",
     "An exact calculation showed a small but nonzero floor. The residual never reaches zero once the program's source term is switched on."),
    ("September 2026", "What picks the geometry",
     "Two-way couplings decide which observers are admissible, and complementary couplings decide the geometry.",
     "The second half was refuted by a control experiment. Consistency favours two-way couplings; it does not pick which one."),
    ("October 2026", "Theorem sheet errata",
     "Several entries in the program's theorem sheets, including one statement that read the wrong way round.",
     "Corrected, relabelled where the evidence was weaker than stated, and reissued with an errata list."),
]


def body_corrections(href):
    h = "research/corrections"
    items = "".join(
        f'<div class="rs-corr"><div class="d">{E(d)}</div><h3>{E(t)}</h3>'
        f'<p><b>We said:</b> <span class="was">{E(was)}</span></p><p><b>What is true now:</b> {E(now)}</p></div>'
        for d, t, was, now in CORRECTIONS)
    return f"""{subnav(href, h)}
<article class="rs-doc"><div class="wrap col">
<h1>Corrections</h1>
<p class="sub">What we said, what is true now</p>
<p class="lead">Every research program gets things wrong. This one keeps a public record of where, so that a reader can
trust the rest. Nothing is deleted; each claim that changed is listed here with what replaced it.</p>
{items}
</div></article>"""


BUILDERS = {
    "research": (body_overview, "Research: what can an observer never see?",
                 "The Observer Limit Program: a mathematics program about the limits of observation."),
    "research/idea": (body_idea, "The idea, step by step", "The central idea of the Observer Limit Program in plain language, with the mathematics."),
    "research/results": (body_results, "What is proved", "Selected theorems and no-go results of the Observer Limit Program."),
    "research/open": (body_open, "Open questions", "The open questions of the Observer Limit Program."),
    "research/predictions": (body_predictions, "Predictions and papers", "Testable predictions of the Observer Limit Program."),
    "research/corrections": (body_corrections, "Corrections", "Public corrections log of the Observer Limit Program."),
}


def home_band(href):
    """Optional: a band for the studio home page, below the app grid."""
    return (f'<section class="wrap rs-band"><a href="{href("", "research")}">'
            f'<div><div class="k">Research</div><b>What can an observer never see?</b>'
            f'<span>The Hidden Structure Research Group: a mathematics program about the limits of observation.</span></div>'
            f'<span class="go" aria-hidden="true">Explore →</span></a></section>')


def build_research(page, write, href, dist, root):
    """Called once from build.py main(). Copies research.css next to site.css and writes six pages."""
    shutil.copy(os.path.join(HERE, "research.css"), os.path.join(dist, "assets", "research.css"))
    for here, (fn, title, desc) in BUILDERS.items():
        doc = page(here, title, fn(href), SECTION, desc)
        css = href(here, "assets").replace("index.html", "") + "research.css"
        doc = doc.replace("</head>", f'<link rel="stylesheet" href="{css}">\n</head>', 1)
        write(here, doc)
