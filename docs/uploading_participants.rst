Uploading study participants
============================

You can add participants to the study in bulk.

mPACT expects a spreadsheet in Excel 2007-365 (.xlsx) format. It will
use the first worksheet. It looks for a column with the heading "Study
ID", and a column with the heading "Phone Number" (case sensitive). You
can use this `empty sample spreadsheet`_ as a start.

Click the "Upload Study Participants" icon. You will be prompted for the
spreadsheet.

mPACT does not store the phone numbers of participants. It uses the
Telegram API to look up their Telegram ID. It will do this for each
participant.

**NOTE:** The Telegram API will only return the Telegram ID of
participants that have messaged the bot in the past. (Telegram does not
allow bots to look up random people.) Thus, it is important to ask all participants
to directly message the bot if their data is to be linked to the relevant Study ID.
Participants must message the bot prior to the upload, but the upload can be done
more than once with no issues.


.. _empty sample spreadsheet: https://github.com/dimagi/mpact/blob/main/docs/sample/study_participants.xlsx
