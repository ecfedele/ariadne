% --------------------------------------------------------------------------- %
% File:        erauthesis.cls                                                 %
% Author:      E. C. Fedele                                                   %
% Date:        August 16, 2022 - January 10, 2023                             %
% Description: Originally, this class was designed to provide a modified      %
%              thesis class for my time at Arizona State University (ASU).    %
%              However, it has been retooled for use as a generic thesis      %
%              template for Embry-Riddle Aeronautical University              %
% --------------------------------------------------------------------------- %
\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{erauthesis}[2022/08/16]
\RequirePackage{etoolbox}
\newtoggle{project}
\newtoggle{thesis}
\newtoggle{strict}
\DeclareOption{project}{\toggletrue{project}\togglefalse{thesis}}
\DeclareOption{thesis}{\toggletrue{thesis}\togglefalse{project}}
\DeclareOption{strict}{\toggletrue{strict}}
\ProcessOptions\relax
\LoadClass[12pt,titlepage,twoside]{report}

\RequirePackage[includeheadfoot]{geometry}
\RequirePackage{fancyhdr,afterpage,graphicx,textcase}
\RequirePackage{amsmath,amssymb,amsbsy}
\RequirePackage[titles]{tocloft}
\RequirePackage[nottoc]{tocbibind}
\RequirePackage[addtotoc]{abstract}
\RequirePackage[intoc,english]{nomencl}
\RequirePackage{titlesec,xcolor,xpatch,setspace}

% --------------------------------------------------------------------------- %
% Configure basic page geometry and XeLaTeX font options.                     %
% --------------------------------------------------------------------------- %
\geometry{
    top    = 1.00in,
    left   = 1.25in,
    right  = 1.25in,
    bottom = 1.00in
}
\newcommand{\oneandhalfspace} {
  \renewcommand{\baselinestretch}{1.24}\small\normalsize
}


% --------------------------------------------------------------------------- %
% Redefine the titlepage per the ASU Graduate College Format Manual (GCFM).   %
% Add additional options and commands to allow the configuration of the       %
% titlepage as a self-study project rather than a required dissertation.      %
% --------------------------------------------------------------------------- %
\newlength{\threeblanklines}\setlength{\threeblanklines}{0.45 in}
\newlength{\fiveblanklines}\setlength{\fiveblanklines}{0.75 in}
\newlength{\tenblanklines}\setlength{\tenblanklines}{1.50 in}

\makeatletter

\newcommand{\defensemonth}[1]{\renewcommand{\@defensemonth}{#1}}
\newcommand{\@defensemonth}{\tt$\backslash$\string defensemonth}
\newcommand{\gradmonth}[1]{\renewcommand{\@gradmonth}{#1}}
\newcommand{\@gradmonth}{\tt$\backslash$\string gradmonth}
\newcommand{\gradyear}[1]{\renewcommand{\@gradyear}{#1}}
\newcommand{\@gradyear}{\tt$\backslash$\string gradyear}
\newcommand{\chair}[1]{\renewcommand{\@chair}{#1}}
\newcommand{\@chair}{\tt$\backslash$\string chair}
\newcommand{\memberOne}[1]{\renewcommand{\@memberOne}{#1}}
\newcommand{\@memberOne}{\tt$\backslash$\string memberOne}
\newcommand{\memberTwo}[1]{\renewcommand{\@memberTwo}{#1}}
\newcommand{\@memberTwo}{\tt$\backslash$\string memberTwo}
\newcommand{\memberThree}[1]{\renewcommand{\@memberThree}{#1}}
\newcommand{\@memberThree}{\tt$\backslash$\string memberThree}
\newcommand{\memberFour}[1]{\renewcommand{\@memberFour}{#1}}
\newcommand{\@memberFour}{\tt$\backslash$\string memberFour}
\newcommand{\degreeName}[1]{\renewcommand{\@degreeName}{#1}}
\newcommand{\@degreeName}{\tt$\backslash$\string degreeName}
\newcommand{\majorName}[1]{\renewcommand{\@majorName}{#1}}
\newcommand{\@majorName}{\tt$\backslash$\string majorName}
\newcommand{\paperType}[1]{\renewcommand{\@paperType}{#1}}
\newcommand{\@paperType}{\tt$\backslash$\string paperType}

\renewcommand{\maketitle}{
    \doublespace
    \begin{center}
        {\MakeUppercase\@title} \\ by \\ \@author \\
        \vspace{\fiveblanklines}
        \iftoggle{thesis}{
            A \@paperType Presented in Partial Fulfillment \\
            of the Requirement for the Degree \\
            \@degreeName \\
            \vspace{\tenblanklines}
            Approved \@defensemonth\ \@gradyear\ by the\\
            Graduate Supervisory Committee:\\
            \ \\
            \@chair,  Chair\\
            \@memberOne\\
            \@memberTwo\\
            \@memberThree\\
            \@memberFour \\
            \vspace*{\fill}
            EMBRY-RIDDLE AERONAUTICAL UNIVERSITY \\ \@date
        }{}
        \iftoggle{project}{
            An Investigatory Project Supplementing the Studies\\
            of the \@degreeName \ Degree in \@majorName \\
            \vspace*{\fill}
            EMBRY-RIDDLE AERONAUTICAL UNIVERSITY \\ \@date
        }{}
    \end{center}
    \thispagestyle{empty}
    \clearpage
}

\makeatother

% --------------------------------------------------------------------------- %
% Configure the table of contents, as well as other lists.                    %
% --------------------------------------------------------------------------- %
\renewcommand\abstractname{ABSTRACT}
\renewcommand\contentsname{TABLE OF CONTENTS}
\renewcommand\listtablename{LIST OF TABLES}
\renewcommand\listfigurename{LIST OF FIGURES}
\renewcommand\nomname{NOMENCLATURE}
\renewcommand{\cftchapfont}{\normalfont}
\renewcommand{\cftchappagefont}{\normalfont}

\iftoggle{strict}{
  \titleformat{\chapter}[block]{\normalsize\filcenter}{}{1em}{}
}{
  \titleformat{\chapter}[block]{\normalsize\bfseries\filcenter}{}{1em}{}
}

\makeatletter
\patchcmd{\@chapter}{\addtocontents{lof}{\protect\addvspace{10\p@}}}{}{}{}% LoF
\patchcmd{\@chapter}{\addtocontents{lot}{\protect\addvspace{10\p@}}}{}{}{}% LoT
\makeatother

% Configure ToC spacing and separator dot placement
% ---------------------------------------------------------------------------
\titlespacing*{\chapter}{0pt}{-50pt}{40pt}
\renewcommand{\cftchapdotsep}{1.7}
\renewcommand{\cftchapleader}{\cftdotfill{\cftchapdotsep}}
\renewcommand{\cftpartdotsep}{1.7}
\renewcommand{\cftpartleader}{\cftdotfill{\cftpartdotsep}}
\renewcommand{\cftsecdotsep}{1.7}
\renewcommand{\cftsubsecdotsep}{1.7}
\renewcommand{\cfttabdotsep}{1.7}
\renewcommand{\cftfigdotsep}{1.7}

\cftsetindents{chapter}{1.5em}{1.5em}
\cftsetindents{section}{3.0em}{2.3em}
\cftsetindents{subsection}{5.3em}{3.2em}
\setlength{\cftbeforepartskip}{0truept}
\setlength{\cftbeforechapskip}{0truept}

% Add contents and page header to ToC, LoT and LoF.
% ---------------------------------------------------------------------------
\addtocontents{toc}{{\hfill Page\bigskip\par}}
\addtocontents{lot}{{Table\hfill\hfill Page\bigskip\par}}
\addtocontents{lof}{{Figure\hfill\hfill Page\bigskip\par}}

% Redefine \tableofcontents to automatically construct the ToC in a specific
% format (Abstract-LoT-LoF-Nomen-CHAPTER-Mainmatter)
% ---------------------------------------------------------------------------
\let\toccopy\tableofcontents
\newcommand{\nomenpath}[1]{\def\nomenfn{#1}}
\newcommand{\abstrpath}[1]{\def\abstrfn{#1}}
\renewcommand{\tableofcontents}{
    \pagenumbering{roman}
    \input{\abstrfn}
    \input{\nomenfn}
    \toccopy
    \listoftables
    \listoffigures
    \printnomenclature
    \addtocontents{toc}{\protect CHAPTER \protect\par}
    \clearpage
    \pagenumbering{arabic}
}

\makeatletter
\patchcmd{\l@chapter}
    {\cftchapfont #1}
    {\cftchapfont {#1}}
    {}
    {}
\makeatother
\renewcommand\cftchapfont{\normalsize\MakeUppercase} 


\setlength{\cftbeforelottitleskip}{-64.0truept}
\setlength{\cftafterlottitleskip}{0truept}
\renewcommand{\cftlottitlefont}{\hfill\normalsize\rm}
\renewcommand{\cftafterlottitle}{\hfill}
\setlength{\cftbeforeloftitleskip}{-64.0truept}
\setlength{\cftafterloftitleskip}{0truept}
\renewcommand{\cftloftitlefont}{\hfill\normalsize\rm}
\renewcommand{\cftafterloftitle}{\hfill}


% --------------------------------------------------------------------------- %
% Configure the section headers.                                              %
% --------------------------------------------------------------------------- %
\renewcommand{\abstractnamefont}{\normalsize\MakeUppercase}
\patchcmd{\abstract}{\null\vfil}{\null\vspace{-50pt}}{}{}