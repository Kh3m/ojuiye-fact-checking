"""
knowledge_base.py

Real, verifiable document corpus for OjuIye, sourced from actual public
INEC and Yiaga Africa statements ahead of Nigeria's 2027 general election.

Each entry is a paraphrase of a real, dated, publicly reported statement,
not a verbatim copy, with the original source and date kept in the
"source_detail" field for traceability back to where it came from.

Each document is a dict with:
    id            - unique identifier
    source        - trusted source label used by the signing/defense layer
                     ("INEC" or "Yiaga")
    source_detail - who said it, and when, for human traceability
    title         - short title
    text          - the paraphrased content the retriever searches over
"""

LEGITIMATE_DOCS = [
    {
        "id": "doc_001",
        "source": "INEC",
        "source_detail": "Statement by National Commissioner Mohammed Kudu Haruna, 3 July 2026",
        "title": "INEC extends Continuous Voter Registration by two weeks",
        "text": (
            "INEC extended the nationwide Continuous Voter Registration exercise "
            "by two weeks, moving the deadline from 10 July to 24 July 2026, to "
            "give more eligible Nigerians the chance to register ahead of the "
            "2027 general elections. The commission also introduced an online "
            "self-service registration option for first-time voters, allowing "
            "biometric capture from a personal device without visiting an INEC "
            "office. INEC said the decision followed a review of the ongoing "
            "exercise and feedback from state offices, political parties, and "
            "civil society groups."
        ),
    },
    {
        "id": "doc_002",
        "source": "INEC",
        "source_detail": "Reporting on INEC's Continuous Voter Registration close, 25-26 July 2026",
        "title": "Continuous Voter Registration closes with 6.88 million new registrants",
        "text": (
            "The Continuous Voter Registration exercise closed on 26 July 2026 "
            "after registering 6,885,330 new prospective voters across three "
            "phases conducted between August 2025 and July 2026. INEC said the "
            "second phase was briefly suspended in April 2026 to clean up the "
            "register after publication for claims and objections, and that the "
            "provisional register would be displayed in August for Nigerians to "
            "verify their details."
        ),
    },
    {
        "id": "doc_003",
        "source": "INEC",
        "source_detail": "Statement by INEC Chairman Prof. Joash Amupitan, early September 2026",
        "title": "INEC voter register approaches 100 million ahead of 2027 polls",
        "text": (
            "INEC Chairman Prof. Joash Amupitan announced that the national "
            "voter register was approaching 100 million, following 10,772,421 "
            "new registrations recorded during the Continuous Voter Registration "
            "exercise, subject to ongoing verification through the Automated "
            "Biometric Identification System. He announced plans for a real-time "
            "election readiness tracker to monitor logistics, staff training, "
            "and electoral technology preparations across all 36 states and the "
            "Federal Capital Territory ahead of the 2027 general elections."
        ),
    },
    {
        "id": "doc_004",
        "source": "Yiaga",
        "source_detail": "Pre-election press conference, Osogbo, 13-14 August 2026",
        "title": "Yiaga Africa deploys observers ahead of Osun governorship election",
        "text": (
            "Ahead of the 15 August 2026 Osun State governorship election, "
            "Yiaga Africa announced it would deploy 300 stationary and 32 "
            "mobile observers across all 30 local government areas. The "
            "organisation said it would use its Process and Results "
            "Verification for Transparency methodology alongside its Election "
            "Result Analysis Dashboard, ERAD 2.0, to independently track "
            "polling-unit result sheets uploaded to INEC's electronic results "
            "portal. Yiaga said the dashboard would not collate results or "
            "declare a winner, only assess the availability, timeliness, and "
            "completeness of uploaded result sheets."
        ),
    },
    {
        "id": "doc_005",
        "source": "Yiaga",
        "source_detail": "Post-election press conference, Osogbo, statement by Dr Asmau Maikudi, August 2026",
        "title": "Yiaga Africa says Osun election shows INEC can deliver a credible process",
        "text": (
            "Following the Osun State governorship election, Yiaga Africa said "
            "the process demonstrated that INEC could meet a high operational "
            "standard and transmit results transparently under the Electoral "
            "Act 2026. The organisation reported that 48 percent of its sampled "
            "polling units began accreditation and voting by 8:30 a.m., rising "
            "to 96 percent by 9:30 a.m., and that the Bimodal Voter "
            "Accreditation System functioned properly in about 80 percent of "
            "polling units, with malfunctions in the remaining 20 percent "
            "resolved on the day. Yiaga said INEC's task was to turn the "
            "lessons from Osun into consistent national standards ahead of "
            "2027."
        ),
    },
    {
        "id": "doc_006",
        "source": "Yiaga",
        "source_detail": "Statement ahead of Ekiti governorship election, June 2026",
        "title": "Yiaga Africa deploys 272 observers for Ekiti governorship poll",
        "text": (
            "Ahead of the Ekiti State governorship election, Yiaga Africa "
            "announced the deployment of 272 election observers to support "
            "independent verification of procedures and official results. "
            "The organisation said comparing electronically entered figures "
            "against scanned result sheets uploaded to INEC's results portal "
            "could strengthen public confidence in the process. Voting was "
            "expected across 2,445 polling units in the state's 16 local "
            "government areas, with 1,059,360 registered voters."
        ),
    },
]
