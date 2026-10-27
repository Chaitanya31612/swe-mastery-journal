# Follow the execution

Trace page request → allowed server read → serialized props → interactive button → server mutation → permission check → database change → deliberate revalidation → visible result.

router.refresh requests a fresh server-component payload, but a server-side cached read may still return old data. Choose revalidatePath/tag or another data policy according to the exact version.

Test the mutation then read from a fresh session as well as the current page.