class ApplicationController < ActionController::API
  rescue_from ActiveRecord::RecordNotFound do
    render json:{error:'Access or source unavailable'},status: :not_found
  end
  rescue_from Ai::InvalidResult do
    render json:{error:'Invalid training request'},status: :unprocessable_entity
  end
end
