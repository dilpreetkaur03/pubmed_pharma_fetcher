import pytest
from pubmed_pharma_fetcher.parser import parse_pubmed_xml

def test_parse_pubmed_xml_minimal():
    # Minimal valid PubMed XML with one article
    xml = """
    <PubmedArticleSet>
      <PubmedArticle>
        <MedlineCitation>
          <PMID>123456</PMID>
          <Article>
            <ArticleTitle>Test Paper Title</ArticleTitle>
            <AuthorList>
              <Author>
                <LastName>Smith</LastName>
                <ForeName>John</ForeName>
                <AffiliationInfo>
                  <Affiliation>Acme Biotech, Inc.</Affiliation>
                </AffiliationInfo>
              </Author>
            </AuthorList>
            <Journal>
              <JournalIssue>
                <PubDate>
                  <Year>2024</Year>
                  <Month>05</Month>
                  <Day>01</Day>
                </PubDate>
              </JournalIssue>
            </Journal>
          </Article>
        </MedlineCitation>
      </PubmedArticle>
    </PubmedArticleSet>
    """
    papers = parse_pubmed_xml(xml)
    assert len(papers) == 1
    paper = papers[0]
    assert paper.pubmed_id == "123456"
    assert paper.title == "Test Paper Title"
    assert paper.authors[0].name == "John Smith"
    assert paper.authors[0].affiliations[0].name == "Acme Biotech, Inc."
