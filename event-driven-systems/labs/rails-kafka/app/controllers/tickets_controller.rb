# Local training API. Add authentication and authorization before real exposure.
class TicketsController < ApplicationController
  def health
    render json: {status: 'ok'}
  end

  def show
    ticket = Ticket.find(params[:id])
    render json: {id: ticket.id, status: ticket.status, version: ticket.event_version,
                  projection_count: ReportingProjection.where(ticket_id: ticket.id).count}
  end

  def complete
    ticket = CompleteTicket.call(params[:id])
    render json: {id: ticket.id, status: ticket.status, version: ticket.event_version}
  end
end
