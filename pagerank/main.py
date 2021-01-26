import pagerank
# print(pagerank.transition_model({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},"1.html",0.85))
samples=pagerank.iterate_pagerank({"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}},0.85)
print(samples)
