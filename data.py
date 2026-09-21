"""Fabricated psychiatry follow-up encounter (no real patient) + an AI-scribe draft seeded with errors."""

PATIENT = {"name": "Maya R.", "age": 34, "sex": "F", "visit": "Outpatient psychiatry follow-up, 6 weeks after starting sertraline"}

# (time, speaker, text)  DR = Dr. Okafor (psychiatrist), PT = patient
_T = [
("00:00","DR","Hi Maya, good to see you. It's been about six weeks since we started the sertraline. How have things been overall?"),
("00:09","PT","Honestly, a little better. Not great, but I'm not crying in the car before work anymore, so that's something."),
("00:18","DR","That's real progress. If you had to put your mood on a zero to ten, ten being your best self, where are you today?"),
("00:26","PT","Maybe a five? Last time I think I said a two or three."),
("00:31","DR","Okay. And how has your sleep been since we started the medication?"),
("00:36","PT","A little better. I fall asleep faster than I used to, but I still wake up around four in the morning most days and can't get back to sleep."),
("00:47","DR","How many nights a week would you say you're waking early like that?"),
("00:51","PT","Five, maybe six. It's pretty much every night."),
("00:55","DR","Are you taking anything to help with sleep?"),
("00:58","PT","My primary care doctor gave me trazodone, fifty milligrams, back in July. I take it maybe two or three nights a week when it's really bad."),
("01:09","DR","Good to know, I'll add that to your list. Does it help?"),
("01:13","PT","It knocks me out, but I feel groggy the next morning so I don't love taking it."),
("01:19","DR","What about energy during the day?"),
("01:22","PT","Still low. I get through work but I'm exhausted by two or three in the afternoon."),
("01:29","DR","And your ability to focus at work?"),
("01:32","PT","That's actually improved. I'm getting through my inbox again. My manager noticed, which was nice."),
("01:40","DR","Are you still enjoying things? Last time you said you'd stopped painting."),
("01:45","PT","I picked up a brush once. Didn't finish anything. I'm not really excited about it yet, but I didn't hate it."),
("01:54","DR","That's a start. Anything going on at work or at home that's been weighing on you?"),
("02:00","PT","My grandmother passed away three weeks ago. She basically raised me. I went to the funeral in Ohio and I've kind of been in a fog since."),
("02:12","DR","I'm so sorry, Maya. That's a huge loss, especially with everything else you've been carrying. How has the grief been sitting with the depression?"),
("02:22","PT","It's hard to separate them. Some days it's sadness about her, some days it's just the same heaviness as before."),
("02:31","DR","Did you miss any work around that?"),
("02:33","PT","Three days for the funeral. My manager was understanding."),
("02:38","DR","Let's talk about the anxiety. You were having panic attacks a couple of times a week in the spring."),
("02:44","PT","I've only had one in the last month, and it was mild. Mostly I just get the tightness in my chest when I think about deadlines."),
("02:54","DR","And the worry itself, the constant background worry?"),
("02:58","PT","Still there, but it's quieter. Like the volume is turned down."),
("03:04","DR","How about alcohol these days?"),
("03:07","PT","Weekends mostly. Three, maybe four beers on a Friday and Saturday night. Nothing during the week."),
("03:15","DR","Has that changed from before?"),
("03:17","PT","It's about the same. Maybe a little more since Grandma died."),
("03:22","DR","Any cannabis, or anything else?"),
("03:24","PT","I'll take a THC gummy once in a while to sleep, maybe once every couple of weeks. No other drugs."),
("03:32","DR","Okay. And caffeine?"),
("03:34","PT","Two coffees in the morning. Sometimes an energy drink in the afternoon, which I know isn't helping the sleep."),
("03:42","DR","I need to ask the harder questions. Have you had any thoughts of hurting yourself or that you'd be better off dead?"),
("03:50","PT","Not like planning anything. Sometimes I think it'd be easier to just not wake up. But I wouldn't do anything. I have my kids."),
("04:00","DR","Thank you for being honest. Have those thoughts been more or less frequent than when we first met?"),
("04:06","PT","Less. It was almost every day before. Now it's maybe once a week, usually late at night."),
("04:13","DR","Any thoughts of hurting anyone else?"),
("04:15","PT","No, never."),
("04:17","DR","Do you have access to any firearms at home?"),
("04:20","PT","My husband keeps a handgun in the nightstand. It's his, but it's not locked up or anything."),
("04:27","DR","I'd like us to talk about that. When someone is having the kind of thoughts you described, even without a plan, having a gun that accessible raises the risk. Would you be willing to ask him to lock it in a safe or store it somewhere else for now?"),
("04:43","PT","I can talk to him. He'd probably be okay with a safe. I don't want to promise he'll move it out of the house."),
("04:50","DR","That's fair. Let's have that conversation and check back next visit. Now, how have you tolerated the sertraline? Any side effects?"),
("04:59","PT","The first two weeks I was nauseous every morning, but that went away. The thing that's still bothering me is my sex drive is basically gone. My husband's been patient about it, but it's frustrating."),
("05:13","DR","That's a common one and it's worth taking seriously. We can talk about options. Any headaches, jitteriness, GI issues now?"),
("05:20","PT","No, none of that anymore."),
("05:23","DR","Are you taking it every day?"),
("05:25","PT","Every morning with breakfast. I've missed maybe two doses total."),
("05:30","DR","Great. And you're still on the fifty milligram dose?"),
("05:33","PT","Yes, fifty."),
("05:35","DR","Did you get connected with the therapist we referred you to?"),
("05:38","PT","I called. They put me on a waitlist. They said probably six to eight weeks before I could get an intake."),
("05:46","DR","Okay, let's see if we can find something faster. Any plans for pregnancy in the next year? I ask because it changes how we think about medications."),
("05:54","PT","No, we're done. I'm on the pill."),
("05:57","DR","Your PHQ-9 from today came back at fourteen, which is down from nineteen at your first visit. So that lines up with what you're describing. Partial response."),
("06:08","PT","That sounds right."),
("06:10","DR","Here's what I'm thinking. The sertraline is helping but you're only partway there. I'd like to increase it to one hundred milligrams. The nausea usually doesn't come back with the increase, but it can, and I want you to call me if it does."),
("06:25","PT","Okay. What about the sex drive thing? Will more make that worse?"),
("06:30","DR","It might. Let's give the hundred milligrams four weeks. If the libido issue is still a problem then, we can talk about adding bupropion or switching. I don't want to change two things at once."),
("06:43","PT","That makes sense."),
("06:45","DR","For sleep, cut the afternoon energy drink and keep the trazodone for the rough nights. I'd rather not add a third medication right now."),
("06:54","PT","Okay."),
("06:55","DR","Given the thoughts you mentioned, I want to put together a safety plan with you before you leave. And I'll give you the 988 number to save in your phone. Can we do that?"),
("07:06","PT","Yeah, that's fine."),
("07:08","DR","Also, the loss of your grandmother, I think grief support would help. There's a group through the hospital that meets Tuesday evenings. I'll put the information in your after-visit summary."),
("07:19","PT","I'd be open to that."),
("07:21","DR","Let's plan on seeing each other again in four weeks. Sooner if the thoughts get worse or if you have any trouble with the higher dose."),
("07:31","PT","Four weeks. Okay."),
("07:33","DR","Anything else on your mind today?"),
("07:35","PT","No, I think that's everything. Thank you."),
]
TRANSCRIPT = [{"id": f"T{i+1:02d}", "t": t, "speaker": s, "text": x} for i, (t, s, x) in enumerate(_T)]

# AI-scribe draft. Each claim is one verifiable sentence. Ground-truth error type is recorded
# in `seed` (for evaluating Jev), never shown to the model.
#   seed values: ok | contradicted | hallucinated | ambiguous | observation (MSE items not verifiable from audio)
DRAFT = [
 {"section": "Chief Complaint / Reason for Visit", "claims": [
   ("Follow-up for major depressive disorder and generalized anxiety disorder, six weeks after initiation of sertraline.", "ok"),
 ]},
 {"section": "Interval History", "claims": [
   ("Patient reports overall improvement in mood, rating it 5/10 today compared with 2-3/10 at the prior visit.", "ok"),
   ("She reports she is no longer tearful before work.", "ok"),
   ("Sleep has improved.", "ambiguous"),
   ("Appetite has improved and she has regained some weight.", "hallucinated"),
   ("Energy remains low, with fatigue by mid-afternoon.", "ok"),
   ("Concentration at work has improved, and this has been noticed by her manager.", "ok"),
   ("Anhedonia is resolving; she has resumed painting regularly.", "contradicted"),
   ("She reports a significant stressor: her grandmother, who raised her, died three weeks ago, and she attended the funeral out of state.", "ok"),
   ("She missed one week of work for the funeral.", "contradicted"),
 ]},
 {"section": "Anxiety", "claims": [
   ("Panic attacks have resolved.", "ambiguous"),
   ("Background worry persists but is reduced in intensity.", "ok"),
 ]},
 {"section": "Substance Use", "claims": [
   ("Patient denies alcohol use.", "contradicted"),
   ("She denies cannabis or other illicit drug use.", "contradicted"),
   ("Caffeine intake is two cups of coffee in the morning and occasionally an afternoon energy drink.", "ok"),
 ]},
 {"section": "Safety Assessment", "claims": [
   ("Patient denies suicidal ideation.", "contradicted"),
   ("She denies homicidal ideation.", "ok"),
   ("Patient agreed to remove the firearm from the home.", "ambiguous"),
   ("Safety plan completed and 988 crisis line provided.", "ok"),
 ]},
 {"section": "Medications and Tolerability", "claims": [
   ("Current medication: sertraline 100 mg daily.", "contradicted"),
   ("Adherence is good, with approximately two missed doses in six weeks.", "ok"),
   ("She is tolerating sertraline well without side effects.", "contradicted"),
   ("Initial nausea during the first two weeks has resolved.", "ok"),
 ]},
 {"section": "Psychosocial and Family History", "claims": [
   ("Family history is significant for bipolar disorder in her mother.", "hallucinated"),
   ("She is currently engaged in weekly cognitive behavioral therapy.", "contradicted"),
   ("She is not planning pregnancy and uses oral contraception.", "ok"),
 ]},
 {"section": "Mental Status Examination", "claims": [
   ("Well groomed, cooperative, with good eye contact.", "observation"),
   ("Affect is constricted but reactive.", "observation"),
   ("Thought process is linear and goal directed; no evidence of psychosis.", "observation"),
 ]},
 {"section": "Assessment", "claims": [
   ("PHQ-9 today is 14, down from 19 at the initial visit, consistent with partial response to sertraline.", "ok"),
   ("Major depressive disorder, recurrent, moderate, with partial response; generalized anxiety disorder, improving; bereavement.", "ok"),
 ]},
 {"section": "Plan", "claims": [
   ("Increase sertraline to 100 mg daily.", "ok"),
   ("Add bupropion for sexual side effects.", "contradicted"),
   ("Discontinue trazodone.", "contradicted"),
   ("Reduce afternoon caffeine.", "ok"),
   ("Referral to hospital grief support group.", "ok"),
   ("Return to clinic in six weeks, sooner if symptoms worsen.", "contradicted"),
 ]},
]
_n = 0
def _claims():
    global _n
    for s in DRAFT:
        for text, seed in s["claims"]:
            _n += 1
            yield {"id": f"C{_n:02d}", "section": s["section"], "text": text, "seed": seed}
CLAIMS = list(_claims())

# Transcript facts the draft OMITS that a psychiatrist would expect in the note (ground truth for the reverse check).
OMISSION_TRUTH = {"T10": "trazodone 50 mg from PCP", "T44": "handgun unlocked in nightstand", "T48": "decreased libido on sertraline",
                  "T34": "THC gummy every couple of weeks", "T40": "passive SI ~weekly, late at night", "T56": "waitlisted 6-8 wk for therapy"}
