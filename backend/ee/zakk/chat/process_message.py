from ee.zakk.server.query_and_chat.models import OneShotQAResponse
from zakk.chat.models import AllCitations
from zakk.chat.models import LLMRelevanceFilterResponse
from zakk.chat.models import ZakkAnswerPiece
from zakk.chat.models import QADocsResponse
from zakk.chat.models import StreamingError
from zakk.chat.process_message import ChatPacketStream
from zakk.server.query_and_chat.models import ChatMessageDetail
from zakk.utils.timing import log_function_time


@log_function_time()
def gather_stream_for_answer_api(
    packets: ChatPacketStream,
) -> OneShotQAResponse:
    response = OneShotQAResponse()

    answer = ""
    for packet in packets:
        if isinstance(packet, ZakkAnswerPiece) and packet.answer_piece:
            answer += packet.answer_piece
        elif isinstance(packet, QADocsResponse):
            response.docs = packet
            # Extraneous, provided for backwards compatibility
            response.rephrase = packet.rephrased_query
        elif isinstance(packet, StreamingError):
            response.error_msg = packet.error
        elif isinstance(packet, ChatMessageDetail):
            response.chat_message_id = packet.message_id
        elif isinstance(packet, LLMRelevanceFilterResponse):
            response.llm_selected_doc_indices = packet.llm_selected_doc_indices
        elif isinstance(packet, AllCitations):
            response.citations = packet.citations

    if answer:
        response.answer = answer

    return response
