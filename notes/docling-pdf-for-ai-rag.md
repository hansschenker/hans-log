---
slug: docling-pdf-for-ai-rag
title: Docling — prepare pdf and other doc formats for working with AI and RAG
date: 2026-06-29
tags: [AI, RAG, Docling, PDF, document-parsing]
source: yt
---

## TL;DR

Docling is an IBM open-source library that converts PDFs, Word docs, and other document formats into clean, structured output (Markdown, JSON) ready for AI and RAG pipelines. It handles complex layouts including tables, images, and multi-column text that naive PDF extractors mangle. The key value is getting high-quality chunks into your vector store with minimal preprocessing noise.

## Key Concepts

- **Docling** — IBM open-source doc parser: PDF, DOCX, PPTX, HTML → Markdown / JSON
- **Layout analysis** — understands columns, headers, tables, figures structurally
- **Table extraction** — preserves table structure as proper Markdown or JSON, not flat text
- **Image OCR** — extracts and describes embedded images
- **Chunking** — outputs semantically coherent chunks, not arbitrary character splits
- **RAG pipeline fit** — clean output → better embeddings → better retrieval accuracy

## Content

_Add synthesized content here after watching._

## Claude Summary

_Paste or link Claude summary here._

## NLM

_Paste or link NotebookLM study guide here._

## Recall.ai

_Paste or link Recall.ai summary here._

## Source

https://www.youtube.com/watch?v=-OM3pqCL8ek&list=PLDWmb8v30mVo&index=21

## Notes

So we will solve that. That's not a problem. All right, so what are we going to
see today? First, we're going to have a short intro like meeting Docling and then just seeing a
bit of the functionality, what it is about and taking a peek under the hood, seeing
how it works. And then towards the end, we have a section also where we explore a bit of
the journey, how we got here, what lies ahead and a bit of the community aspects as well.
And that will be it. So first of all, the good thing about
us building Docling is that it's very, very helpful in that everybody uses documents.
There is not one person that does not use documents in their day work.
So all types of documents, all formats, all constellations you can imagine, many, many modalities going
into that. So it's not like pure text. You have images, you have tables, you have different types of stuff.
Plus, you also have other types of unstructured data as well besides documents. So one thing with documents is that working
with them is very, very complicated. So just picking an example, think about PDF.
It's a notoriously evil format to work with. And that makes one point.
And the other important point is that the modern LLM technology we have does not natively
understand this like PDF, for example. It will not natively understand it.
What it can understand is text. So what we do nowadays, mostly what people
do is trying to build these bridges between these two things. But this bridging really comes with significant sacrifices.
And sacrifices can be in terms of cost, can be in terms of quality, can be
in terms of you losing sovereignty over your data, and many other things.
So that's pretty much exactly where Docling comes into the picture, quite literally.
Sorry, this does not work with the clicker.
Why is Docling useful? First of all, it is open source. You don't have to pay for it, and
it is bound to be open source forever.
Secondly, it includes our advanced AI models that we have been building for many, many years,
and we have been involving, and which are made specially for the task of document understanding.
It supports many different formats. So it's a single tool to kind of rule them all, if you like.
And it works with a unified representation that is rich, is not really just naive plain
text, and it's LLM friendly, as we will be seeing going forward. What's more, it all runs locally.
You don't need to give your data to anybody for using Docling.
And last but not least, we've made sure to put it pretty much everywhere, so no matter where you are comfortable working at, you
can just pick Docling from that environment, and you're off to the races.
So, where do we stand today? We stand at a situation where we are getting very good traction.
We are 60,000 GitHub stars. We have more than, we have close to 7 million downloads per month on PyPI.
We have been the number one repository on GitHub across all dimensions for a very long time.
We have been the number one model, number one data set on Hugging Face, to the
extent that the Hugging Face CEO called it the Grand Slam of trending. We are within the 300 top repositories ever
in terms of stars , and we are part of the Linux Foundation, namely of the AI and Data Foundation under that umbrella.
So, just to give you a quick glimpse as we're going through the discussion to keep in mind where the project sits at.
But how does the project actually look like? How do we use it? So, in principle, you can use Docling in
many different ways, as I outlined earlier. You can use it, for example, as CLI.
You just pip install Docling, and in one command, you can convert documents, and we'll see
what that looks like. Or we have a very powerful SDK that essentially allows you to build any kind of
workflow you want. But also, you can use it as an MCP tool for your agents.
You can use it as an API service, as a plugin for all types of LangChains LlamaIndex's, CrewAIs, Haystacks, and whatever
out there. So, you can just, in one line, use the functionality. Okay.
So, let's have a quick look how the CLI, for example, looks like. And for that, I am sharing here a
quick video where we start with a document, and you see what the document can entail.
For example, multiple columns. It can have tables, figures.
It can have different types of captions, paragraphs, and what have you.
So, in one line, we're just saying, Docling, for example, I want to convert to HTML in this example.
And you will see that in a couple seconds, we get back the HTML, also the
included images. But what we see in the HTML is, importantly, that the whole document structure is maintained,
right? So, you have the paragraphs. You have the headings. You have what was a list, all the different figures.
And, importantly, as we move towards the more, say, challenging aspects of the document, you can see that there's multi-column spans that are
retained in tables. And these kind of intricacies that very often are just really overseen by, you know, kind
of naive tooling out there. All right. So, let's move on to the next one.
So, one of the reasons why people consider Docling is also around the cost, right?
So, what you see here is, in principle, the biggest PDF dataset created by Hugging Face.
It's called Find PDFs, and they used two technologies for building that.
And you can see that Docling, and by the way, the slides are already available online.
It's just on GitHub, so we can share them, but you will find them also later. And you can see that the Docling technology
is 50 times more cost effective than the other VLM that was used there. Just to give you an understanding, right, how
they were able to go to, like, half a trillion PDFs parsed with that.
Okay. Another interesting collaboration, besides what I just showed with Hugging Face, is also, like, with NVIDIA,
where this is from, actually, from this year, where Jensen was presenting our collaboration on the
data side. This was, I believe, more on the actual structured data, part of the broader team here
at Rüschlikon. But we are also collaborating very strongly around the unstructured data with Docling and with building
new models and so on and so forth. So, very, very interesting to see the, you know, fruits out of this technology.
So, now, what about, you can ask me, what about the other technologies that are out there, right?
Why don't we just use, say, a plain, very simple, fast technology, right?
So, yes, you could use, for example, a low-level PDF parser, like pypdfium or this type of tools.
But what you will see is that, in principle, you will get very, very low quality. You will have no structure.
They will be incomplete. Here you can see, like, tables. Forget about it. And different kind of modalities, completely, like, ignored
or misinterpreted. So, if you want to do anything of essence with this data, yeah, you get, you
start on the wrong foot, right? Imagine just feeding this further down, different types
of defects here. But also, if you consider very big models, and I know, okay, this is a bit
older models here that we are showing. The principle still remains.
Even big models, they're trained to do pretty much everything. So, they're not necessarily very good at doing
this one task of document understanding, right? So, you can see, like, a dozen billion parameter models messing with the titles or the
structure of the table. So, this just goes to tell you that you have to have a sweet spot in
that area. Now, what you see here is, in principle, you know, the known story of vegetative electron
microscopy. It's, like, a very deeply studied domain out
there. Unfortunately, it's a non-existing one. But just rather came to be because, you
know, some parser parsed these two columns as one. And then dozens and dozens of researchers made
papers that were peer-reviewed by other researchers. And they're published.
And, you know, we have now many of these documents talking about this topic. Okay.
All right. So, just goes to tell you that, you know, if you have poor quality in your
data and your document pipelines, this is really trickling down and causing a lot of problems
downstream. And obviously, Docling can address this nicely. Okay.
What else can quality look like? We all know our interactions with all of
these chat environments and how we make a question and we get back an answer. That always looks very, very affirmative, you know,
very confident. And oftentimes, we just leave it at that. And we have no clue whatsoever whether it
actually stands where it's correct or not. Right? So, what can be a very powerful feature that Docling can power is, like, you make
a question, you get back an answer. But crucially, you also get visual grounding.
You know, you can know where from the answer originates in the document and can validate.
So, you, as a human, are actually kept in the loop. And that gives you a handle to go
check. And, you know, this is the element that, in my opinion, can bring more trust into
an AI system. And this is a very important aspect nowadays, I believe.
All right. And maybe just another anecdote. This other aspect of papers that were published
where people were just making prompt injections in white text. So, you know, here people were asking the
reviewer LLMs to not highlight any negative aspects of the paper. So, it is just different ways of telling
you, you know, how you build your document pipeline is very, very important. And it is becoming increasingly critical with all
of the technology that is being built. All right. So, how does Docling work a bit under
the hood? Yeah. So, in principle, this picture summarizes things quite
nicely. What we do is we have these different pipelines that address different types of input document
formats. So, we cover, for example, Microsoft Office formats. We cover, like, pictures, audio, markdown, PDF, different
types of things, right? So, the important decision, the important design feature
here is that we are mapping all of these different formats to a single unified representation.
Which is this column that you see, this light blue column that's called Docling document.
So, that's kind of the core of it is getting from whatever you started from to
this unified representation. Because once that is in place, everybody is very happy because they don't have to care
about PDF anymore. They don't need to know about this document ever originating from a PDF or a Word
document or what have you, right? Now, you can just work with the SDK and take that object, which is a Docling
document, and chunk it in a document native way. And can export it to different formats and
can feed it to your agents. And you can essentially do whatever downstream task
you want from a single place without having to build custom pipelines and post-processing around
everything. So, what's interesting here is that for PDF, for example, which is kind of the challenging
format in this scenario, or images equivalently, we have two options. One is the default pipeline, or the standard
pipeline as we call it, which is an opinionated pipeline where you have different models catering
to different aspects of this whole task. Like OCR, and then there's a layout analysis
model, and there's a table structure model. And at the end, we're putting everything together. And these are essentially the models that we
have been building and iterating on for a very, very long time. And this is more like the production-ready,
essentially, pipeline that is super, super light. It runs on a CPU. You don't need the GPU for this.
And it's very, very stable. And at the same time, what you see a bit as a second line is what
we call the VLM pipeline, which is where we are more and more focused now. Which is essentially the single-shot VLM pipeline
where one single model takes care of all aspects. And essentially, everything is driven by the data
as to how we build this. So, this is the more scalable approach.
It may not be 100% stable at this point as we are working to further
iterations. But in principle, it's the one that is more powerful and the one that we are pushing more going forward.
So, all of this is configurable, as you will see. And you can essentially do it the way you want.
Just a picture of the different components that we have in our internal ecosystem.
When we say Docling, it can mean many different things in terms of, for example, what
you see on the top is Docling Core. It's like the data model, the application API, where I'm driving a lot of these aspects.
We have the conversion and we have different repositories that address different aspects of this whole
ecosystem. Just to show you a bit the breadth of it, it goes from testing, from conversion
scaling, from extensions, and so on and so forth. And part of our actual contributions is also
to other repositories external to Docling, where we're working with frameworks, for example, in their own
repositories. So, as I mentioned earlier, a lot of
what we're driving is around the VLM area, where VLM stands for Vision Language Model, where
essentially you have a single model that does everything. And this model, the speciality here, the differentiator
is that we are making tiny models. We are talking like 256 million parameters.
So, this is like nothing, right? Today, we are talking about trillion model parameters
that people are building. So, a lot of big difference there.
So, these models are so small, but they are very, very specialized, right? So, this can give you essentially both the
quality and the cost effectiveness that you need. So, that was the first iteration that we
got with SmolDocling as a collaboration with Hugging Face. And then we moved on and made the
second iteration called Granite Docling with many more features. And essentially now, as you will see later,
we're building the third most powerful iteration of that as we're going.
So, here you see a bit how that model works. And this is just a space from Hugging
Face, like a demo space. So, it's just showing you a document on the left side.
And how the model is just essentially generating
what used to be called doctags back then. So, essentially a language that pretty much maps
one-to-one to what I mentioned, the unified representation. So, we have our own language of describing
this unified representation. And that used to be called doctags, but now we are in the process of
strengthening it much, much more. And we will come back to it later. I'm very, very excited about that.
So, you see different types of modalities covered, different types of languages here. Also, you have some right-to-left text,
which is also covered. So, we did try to put a lot of this functionality into our models, as you
see. All right. So, moving on.
So, what are the reasons that help Granite Docling stand out?
In principle, one of the main reasons is going to be the sizing that I mentioned earlier.
It's going to be the multi-modal aspect that is able to address different things from
tables, figures, charts, all of the different text
elements, and so on, so forth. All with the bounding boxes, obviously. But also, very importantly, this unified language that
we will come back to. All right. So, just exploring one more interesting feature that
we have on the Docling side. Essentially, we don't want to prescribe too much
around which models you should use or whatsoever. So, in principle, we do allow you to
use other models as well within the Docling framework. And one of the ways that we are
doing this is by having hooks where you, for example, can bring in your favorite expert
model on task X to help you with part of the document. So, what you see here, for example, is
you configure the pipeline very easily to say, look, I want to use that model from
hiding phase, but it could just as well be any model, like a served model as well, for picture annotation.
Because I have this model that's very good for captioning this particular type of diagrams or
what have you. So, this is absolutely possible. And this is something that we see is
super important for providing the modularity and the composability that is needed for real solutions out
there. Essentially, we have many, many, many, many different types of use cases that people are looking
at. Yeah. So, that's an important aspect. You can use other models as well.
We are not prescribing only our models. And here comes essentially a completely different also
way of looking at these problems, which is, you know, what we've been looking at until
now is essentially what we call conversion. Like starting from an existing document and trying
to represent it in a truthful way with our representation. But a different type of problem can be
you don't just start from an existing document, but you actually know very much exactly what parts of the document you're interested in.
So, that's what we call information extraction. And that's a scenario where you may have,
for example, like your invoices or your product sheets or what have you. And you come with a predefined schema where
you say, look, I'm interested in the invoice number. I'm interested in the total value on this
and that. And in principle, you will get out of the document this kind of aspects right away.
So, again, it's a bit of an orthogonal functionality to what we discussed earlier.
But, you know, these two things together, I believe, build a very, very powerful plane for
developing very nice applications there on the document side. And as you imagine, agents could have not
been missing. Everything is around agents nowadays. So, obviously, naturally, we are trying to put
this as a very core focus of what we're doing, because a lot of this is
used in the context of agents. Right. So, that's why we have, for example, the MCP, Docling MCP out there, but also specialized
agents that we provide such that you can, in principle, you know, use Docling from different
agentic environments. And, you know, you also see a different many different logos here, like from CrewAI to
Langflow. So, these are different places where Docling capabilities are essentially already integrated.
So, for example, Langflow, I believe the advanced document parser that the UI supports is directly
Docling. Yeah. So, with that, just let's look at one
last, you know, snapshot of interesting things that have happened recently.
One very nice aspect is that we had directly from the community and interest on the
Java world. And we saw that, you know, Docling being very much a native Python thing.
Oh, actually, this capability is useful, obviously, also from different communities.
Right. So, we were very happy to also help spin off this other initiative around the Java
Docling Java project, which is using the Docling capabilities. As mentioned earlier, we have a very nice
collaboration with NVIDIA as well. Here, you see the announcement they made around
part of the model work that we did together. And many different features that we are constantly
advancing and sharing news on, be it on chart understanding, right, extracting, for example, actual values
from your line charts or pie charts, what have you, to how you parse and many
different things that we're working on. So, that hopefully solves a bit what we
had in the beginning that some people did not know about Docling. So, now you have an idea what Docling
does. What I would like to do next is spend a bit of time on discussing a
bit the community aspect and, you know, how we got here and what was coming next.
All right. So, first of all, how we got here.
So, when it comes to that, I think it definitely helps that this is not our
first rodeo as a team. The team has been building a document understanding capabilities for like decades.
You see, like, this is really not the full list of papers that we've been doing.
It's just a shortened version and that goes up to 2018. I think, in reality, it goes further back.
And, in principle, what this tells you is that the team has a strong competence on
the actual field of computer vision for documents. And this is a very much needed aspect,
right? You cannot just appear in the field and say, look, I built something with an agent
and it's two lines and it solves everything. So, the team's exposure to these problems over
such an extended period of time is part of the elements that have been very important.
And not only that, but also we have been building broader technologies on top of that.
So, for example, before Docling came to be,
the team was working on another project that was called Deep Search. And you see a bit of what it
used to look like back then. So, we're talking like 2021, 22.
And we already had things like advanced multimodal RAG with different types of capabilities in there.
So, we were already talking to customers and exposed to what the customers are interested in,
which sort of use cases would be appealing to them. And, you know, essentially, this experience helps a
lot. So, it was actually through a coincidence that Docling came to existence in 2024.
And what we essentially did is we distilled, we took these models out of the Deep Search, essentially, technology.
We put many more things around it as well. But we were able to reuse a lot of this technology as well.
Crucially, though, what I believe was more important is that we were able to use our
experience and our exposure to these problems and to the user needs on that side.
So, that's very important. I think this aspect is key, right?
Culture, it was mentioned earlier. I think it's so super important. So, if you think of the whole hierarchy
here, essentially, when we open sourced Docling back
in 2024, and I'm saying back in 24, because by today's standards, 2024 is a time
like Stone Age. You know, it was not the most self
explanatory thing to do to go out and open source a key AI technology, right? So, you can imagine that there is dynamics
at play, that it cannot be straightforward necessarily. So, we were fortunate that the standpoint of
the company was strongly shifting towards open source AI strategy, right?
So, that was definitely one aspect. But, you know, I think this is a
bit of also trends that come and go in that sense. So, sometimes you also need this bit of
luck with aligning with the current trend. And then the team is the absolute most
important aspect that we are most thankful, obviously, of having a very, very strong team with
mixed skill set, you know. And if we are to lead in this space of document AI, it is just impossible
to do it if you don't stick to the cutting edge, to the bleeding edge every
single day. And really work at the breakneck speed, it is otherwise, you're just irrelevant in this field
with scale and speed of things happening. So, what has been key in that sense
is that everybody on board has retained a strong growth mentality.
We never know, right? We always need to learn something first, something again, be it from like, you know, this
has been largely a research team, right? With also some experienced software engineering members, but
a team that has a strong research aspect. How can you drive a product that is
meant to, you know, be appealing to developers?
How can you attract developers, right? So, it has to be developer first experience. And that is one of the things that
we had to learn. We're obviously adapting to, as everybody, to the
new agentic and work of way of coding, all things like spec driven development, all things
like that, right? But if I'm to pick up one aspect, that would be really having an entrepreneurial mindset
around everything. And what I mean by that is essentially that we have been cultivating seeds in any
opportunity possible. We have been planting seeds like crazy over a long amount of time and, you know,
knock on that door to talk to that person, pursue that opportunity, follow up on this forever, relentlessly from many, many people on many,
many fronts. So, I think this is so crucial.
And, you know, sometimes if you look back at a certain course of events, you may think, oh, that was actually a lucky moment,
right? Or people talk about serendipity. Oh, that was just pure fortune.
Yes. And you can actually, in a way, create or support your own luck by being so
relentlessly after going after opportunities. So, what we found super interesting, and it
was also discussed earlier very nicely, is that open source has been a great place to
collaborate. So, I think if you look at the collaborations we have had, and it has been
with many different parties at this point, you just see some of the logos here that, in one way or the other, we're collaborating
with, it would have been plainly impossible beside the corporate walls.
Or it would have been so slow that it would be completely irrelevant. So, you know, the scale and the speed
that you can achieve in the open is unique. So, for us, this has been an enabler.
Because the moment you're out, you can talk about your work with everybody. They can get interested in your work.
They want to contribute. Everything moves faster. So important.
And then, obviously, as donating the project to the Linux AI and Data Foundation has also
been very crucial in that, obviously, on the
surface, you get this sort of governance layer, right? Open governance.
You get sort of the framework, how you are supposed to operate. That helps, right? And that gives you some structure on many
aspects. And also, you get some exposure to additional communities and additional opportunities that may be available
through the Linux Foundation. But at the end of the day, I believe the single most important factor is the
trust, the seal of trust that the Linux
Foundation, or obviously also other foundations, right, convey through their logo.
Because a user that is looking at the technologies available out there and trying to pick
between Docling or this other technology or Docling or this other open source technology will also
very much account for the fact that Docling is bound to remain open source forever through
the Linux Foundation. So this is a very, very strong differentiator for many companies around what they actually go
for using, because they don't want to run into this sort of situation where suddenly something
got re-licensed and whoops, or, you know, these things have happened.
All right. So how did we grow? I think at the end of the day,
besides what I've discussed earlier, also by just, you know, showing up, by being there, by
being present in all types of events, sessions, venues, be it online, being in person.
Okay, I put here together a couple of photos. But in principle, we have been very, very
active. And if you ever go to like a Docling workshops repo, it's on GitHub, where you
can find also this presentation, you will see our schedule for this year, for last year, and it's very, very, very dense, right.
So this spreads the message. The message is, thankfully, strong, people are liking
it. And that's how we are now at 60 ,000 stars. And hopefully through your star as well, we
will go to the duck will move a bit towards the upper right side. Okay, now moving a bit to what's next.
Okay, we saw how we got here. Now what's next? I will start with a bit of the
overall what's next, which is the kind of
elephant in the room of the growing, okay, the growing community that we are, you know,
we do appreciate we have, but also the growing AI usage, which is just a global
reality for everybody right now. And you see here just some, some of
the numbers that GitHub was publishing, I believe was two weeks ago or so, where essentially, they were trying to do their own postmortem
and how they are essentially also facing this massive sprawl of issues of pull requests, and
every single maintainer out there is facing those. And it obviously, you know, the larger the
project, the larger the kind of attention it will enjoy and the larger numbers it will face.
So our team, and I believe the whole community is adapting to this reality.
You know, the community numbers are not the numbers that used to be like last year, let alone three or five years ago.
So if people should start thinking about scale,
like sheer scale, and I've heard of, I've had very interesting conversations on that one. And how essentially, you know, even things like
PRs and issues are meanwhile, most likely to be thought like just signals that you can cluster and make something out of.
But yeah, it's a very interesting topic. Okay. But for us, what was also very relevant
is like, there is also a proliferation of different tooling, agents, benchmarks out there, so many
VLMs, you just see some of them up on the top right side that are doing documents, right. So that's another thing that the user is
confronted with right now, and is confronting with managing those, evaluating and so on and so forth.
At the same time, though, for us, this is a massive opportunity to drive the document
AI space across the whole stack. And essentially, from the data model, going to
all the way to the models, to the agents and to the evaluations and metrics. And that's what I will be shortly talking
about and closing with in the next slides, essentially our agenda, our roadmap for the months
to come, which is essentially addressing these aspects. So I'll start from the first one, which
is very, very close to my heart, which is DocLang, which is essentially a standard that
we're putting in place, which is going to be the AI document standard.
So a format that is going to essentially address all of these aspects in a unified
way, and enable all of these AI workflows that people are building nowadays with their documents,
and also the people that make models have to address and so on and so forth.
So we are working with the Linux Foundation to do that. We're working with partners.
We're very happy that NVIDIA signed very recently on that. We're working with ABBYY, a very big OCR company.
So essentially, this is going to be the standard of how people can do AI with
documents. And I'm very, very happy about the work that we're doing there.
How this naturally moves forward is also it directly flows into our new models, which are
going to be very strong models that can leverage these aspects and where we are putting
a lot of innovation from our scientists there as well. So that's something that's going to improve not
only the VLA models, which is essentially the core of our focus, but also we are doing iterations of our individual models of our
standalone pipeline of the standard pipeline. And last but not least, or maybe second
to last, in principle, what we also see is like everybody that makes models nowadays also
feels the need to publish some numbers, and they do. But one of the underlying problems with that
is that the actual even metrics that people report on are not meant for documents.
So it's kind of an ill-posed problem. People are using, you know, sort of tooling from the broader computer vision community history, and
they're just using kind of, you know, people tend to not do the groundwork. Let's summarize like that. And then what we are trying to do
also in that sense is to really, you know, do the groundwork, build the actual metrics
that are native to documents, make it open source, build an evaluation suite, make it very
efficient. So that is also going to be open source very, very soon. And I'm very happy about that as well.
And obviously, and naturally, the company is also trying to capitalize on this being having such
good traction with the community. So it is seeing the value of saying, look, you don't need or not anybody needs
to deploy their own infrastructure on this and having to maintain that. So we are also within IBM making this
an actual managed service, where essentially you will be able to just consume it as an
API very easily. So this is, I believe, a natural step.
And, yeah, that pretty much concludes the talk. If you need to take some messages with
you, you know, it is very easy to use. It helps you automate a lot of your
workflows around documents. It is very cost effective, high quality, and
your data is with you. It never needs to leave your laptop. And you can build all types of applications
that you want with that. And we are really committed to pushing, you
know, the boundaries of standardization of innovation on this document AI space across the whole stack,
as you saw. So, if you will, feel free to, you know, check our community, go to docling.ai,
give us a star, you can join us on Slack, you can join us on GitHub on LinkedIn, you know, follow developments of what
we're doing. And also, you are very much welcome to make contributions and interact with us.
We also have office hours where you can make questions and things like that. Okay. And I also have stickers for whoever wants
to take a Docling with them. So, that's it from my side.
So, thank you for the presentation. That was nice. So, we have a question from the chat,
which is, is there any way for a human to somehow see side by side how
some information from the source has been structured or formatted in the target? Because that would help gain user confidence.
Yes, we have different ways of addressing this
question. In principle, we also have components of TypeScript
that people can, and we also have our Docling serve, which comes with a small UI,
where you can essentially get a very nice visualization of the different elements that are, you
know, constituting a document. And you can see the layout of the document and the reading order and everything.
So, this is something that has not possibly gotten the attention of the whole visualization aspect
in the open source space has not gotten the attention that it may be actually deserving.
So, yeah, but I would still recommend people to have a look at our TypeScript components
and how this can be useful for that. Okay, thank you. Sure.
Thanks a lot. Can you say something about parsing legacy documents like scanned pages, which are a little jagged,
noisy, and so on from the 1980s, without proper formatting, which still contain maybe legacy, in
particular, mathematics, numerics, physics, know how?
Yeah, that's a great question, right? And it kind of brings to surface the complexity of the whole thing.
And you can imagine, the more jagged, the more skewed, the more obscure the writing, at
some point, it becomes impossible also for a human, right? So, there's a continuum to that, but we
are very strongly working on these aspects in many different fronts. So, one of it is essentially a synthetic
data generation. So, we are working on producing different types of artifacts, different types of modalities or artifact
modalities. You just described some of them, right? It could be coffee stains, it could be anything, right? It could be also different types of handwriting.
So, it's something that you have to pretty much address on the data level, ensure that
it's part of the data mix, right? And that's always a bit of an opinionated decision, which aspects we consider important, and also
then also in the evaluation at the end of the day. But definitely, we do see that a lot
of the actual use cases do, you know, relate to such environments, legacy documents, handwritten, and
so on and so forth. That's for sure. So, yeah, great point.
Great presentation. Quick question regarding the DocLang. Do you see that there is a necessity
for specific languages for these use cases rather than using HTML or a more generic thing?
And if so, do you find other applications would also require their own language or are
generic languages sufficient? Yeah, great question. And thanks, because apparently I forgot to mention
some stuff in my presentation. So, yes, we do believe DocLang is catering
to very specific AI specific needs. And these are going to be around aspects
like LLM friendliness, in terms of like token efficiency, in terms of like including the bounding
boxes. You know, it's going to be aspects like these that people do care about for different
reasons in the whole AI space. So, for example, if you look at HTML,
right? If you see, for example, let me just
bring up like the table modality, how tables are done in HTML, for example, it is
not designed for token efficiency. The team has developed a language, which is
proven to be optimal for tables, which is called OTSL already many years ago.
So, essentially, this was built for being optimal in terms of tokens. And it has actually been on top of
that language that then doc tags was produced and out of which then DocLang is essentially
merging. So, it's a sort of natural progression of this whole idea. And then also, if you think about HTML,
you're not able to necessarily easily do what we mentioned around, there is no unique rendering.
So, that also makes it a bit more, you know, less tangible and things like visual
grounding would be done in a different way. So, at the end of the day, it's
different languages built for different purposes. Plus, HTML doesn't have necessarily the concept of
what is a document component, right? It was meant for a visual on an
actual browser. So, it doesn't know the concept of some of these document specific things.
Yeah, I'm very happy to also, you know, follow up offline or later. Hello, missed a few minutes from your presentation.
So, sorry, if you're already answered, but were there some discussions to put this into a
commercial product? I could imagine this is not really a non differentiating thing.
Yes, it is being GA soon. It has already been announced. It's a tech briefing.
So, yes, it's a product that we are starting with. And I'm say starting with because what we're
putting out is essentially the first step, right? It's a super horizontal API service that everybody
can convert documents with in scale. But I believe that it would make sense
to build on top of that, you know, and build more on the same more integrated capability level as well.
How do you mean keeping it closed? We went the other way around.
We started from completely closed. We already were there and we came to
open source. So, yes, this is not going back. This is now. This is now forever public.
Perfect. Thank you very, very much for this interesting presentation.

## Related

- [[rxjs-deep-dive-course]]
