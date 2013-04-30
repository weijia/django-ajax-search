Configuration
=============

The configuration is almost done. All the remains is to define a search function.    
     
Define a new function on the path that you provided for the AJAX_SEARCH_HELPER setting in the previous section. Assuming that the model you want to search is called Article and you wish search the **title** field of every article::

<pre><code>
def search_helper(count, query):
	import itertools
	model_list = Article.objects.filter(title__icontains=query, status=1)
	for L in range(1, count+1):
		for subset in itertools.permutations(words, L):
			count1=1
			query1=subset[0]
			while count1!=len(subset):
				query1=query1+" "+subset[count1]
				count1+=1
			model_list = entry_list | Article.objects.filter(title__icontains=query1, status=1)
	return (model_list.distinct())
</code></pre>
You may stop at the third line to return a very simple list that matches exactly the query provided with the title. The 'for' loops break the search query down and search the parts and various combinations thereof. We suggest you use this method.    
    
Now all you need to do is specify the position of the drop-down menu. Read about it here.
