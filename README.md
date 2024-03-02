# Bdocs

## Write, copy, delete, and higher functions for Cdocs

Cdocs is a contextual help framework. It is read-only. Bdocs is an overlay to Cdocs. It adds the ability to interact with Cdocs roots.

On top of that, Bdocs adds higher level features, including:
* Management of the Cdocs root within a local Git repo
* Searching Cdocs roots
* Rules that allow you to publish content with specificity
* The ability to make private Cdocs roots
* Transformations to be applied to docs as they are returned

Like Cdocs, Bdocs is intended to be a library, not an application. On its own it is not a content management system. However it is straightforward to use Bdocs within an API to create a more complete solution. And the Bdocs design contemplates swapping in custom implementations for individual functions. This flexibility should make it more practical to layer up an application around Bdocs.

Bdocs is on Pypi <a href='https://pypi.org/project/bdocs/'>here</a>.

