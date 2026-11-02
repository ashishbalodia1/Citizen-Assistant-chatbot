import React, { useState } from "react";
import { redeemCoupon } from "../../services/chatApi";

export default function RewardCard({ data, onCouponRedeemed }) {
  if (!data) return null;

  const points = data.points ?? data.user_points ?? 0;
  const badge = data.badge || data.badge_level || "New Guardian";
  const coupons = data.coupons || [];

  const [redeemingId, setRedeemingId] = useState(null);
  const [redeemedCode, setRedeemedCode] = useState(null);
  const [errorMsg, setErrorMsg] = useState(null);

  const nextTierPoints = points < 100 ? 100 : points < 250 ? 250 : 500;
  const progressPercent = Math.min(100, Math.round((points / nextTierPoints) * 100));

  const handleRedeem = async (couponId) => {
    try {
      setRedeemingId(couponId);
      setErrorMsg(null);
      const res = await redeemCoupon(couponId);
      if (res.success) {
        setRedeemedCode({ id: couponId, code: res.voucher_code });
        if (onCouponRedeemed) onCouponRedeemed(res);
      } else {
        setErrorMsg(res.message || "Could not redeem coupon");
      }
    } catch (e) {
      setErrorMsg(e.response?.data?.message || "Failed to redeem coupon");
    } finally {
      setRedeemingId(null);
    }
  };

  return (
    <div className="bg-[#ffffff] border-3 border-black rounded-2xl p-4 shadow-[4px_4px_0px_#000] my-2 max-w-md w-full">
      {/* Header */}
      <div className="flex items-center justify-between border-b-2 border-black pb-2.5 mb-2.5">
        <div className="flex items-center space-x-2">
          <div className="w-9 h-9 rounded-xl bg-[#ffd700] border-2 border-black flex items-center justify-center font-bold text-lg shadow-[2px_2px_0px_#000]">
            🪙
          </div>
          <div>
            <h4 className="text-xs font-bold mario-font text-slate-900">
              COINS & RANK
            </h4>
            <span className="text-[10px] text-[#e52521] font-bold block uppercase">
              ★ {badge}
            </span>
          </div>
        </div>
        <div className="text-right">
          <span className="text-xl font-bold mario-font text-amber-600">
            {points}
          </span>
          <span className="text-[9px] mario-font text-slate-500 block">COINS</span>
        </div>
      </div>

      {/* Progress to next tier */}
      <div className="mb-3.5 bg-slate-50 p-2.5 rounded-xl border-2 border-black shadow-[2px_2px_0px_#000]">
        <div className="flex justify-between text-[10px] mario-font text-slate-700 mb-1">
          <span>NEXT TIER</span>
          <span className="text-[#00a800]">{points} / {nextTierPoints}</span>
        </div>
        <div className="w-full bg-slate-200 h-3 rounded-full border-2 border-black overflow-hidden p-0.5">
          <div
            className="bg-[#ffd700] h-full rounded-full transition-all duration-500 border-r border-black"
            style={{ width: `${progressPercent}%` }}
          />
        </div>
      </div>

      {/* Error alert */}
      {errorMsg && (
        <div className="mb-2.5 p-2 bg-rose-50 border-2 border-rose-600 text-rose-800 text-xs font-bold rounded-xl">
          {errorMsg}
        </div>
      )}

      {/* Coupons list */}
      {coupons.length > 0 && (
        <div>
          <span className="text-[9px] mario-font text-slate-700 block mb-2">
            🍄 TOAD'S ITEM SHOP:
          </span>
          <div className="space-y-2">
            {coupons.map((coupon) => (
              <div
                key={coupon.id}
                className="bg-[#fffdf0] border-2 border-black p-2.5 rounded-xl flex items-center justify-between text-xs shadow-[2px_2px_0px_#000]"
              >
                <div className="pr-2">
                  <div className="font-bold text-slate-900">{coupon.business_name || coupon.business}</div>
                  <div className="text-slate-600 text-[11px] font-medium">{coupon.offer}</div>
                  <span className="text-[10px] font-bold text-amber-700">
                    🪙 {coupon.points_required} COINS
                  </span>
                </div>

                <div>
                  {redeemedCode?.id === coupon.id ? (
                    <div className="bg-[#e6f9ed] border-2 border-black text-emerald-900 px-2 py-1 rounded-lg text-center shadow-[1px_1px_0px_#000]">
                      <span className="text-[9px] mario-font block text-[#00a800]">CODE:</span>
                      <span className="mario-font text-xs font-bold">{redeemedCode.code}</span>
                    </div>
                  ) : (
                    <button
                      onClick={() => handleRedeem(coupon.id)}
                      disabled={redeemingId === coupon.id || points < coupon.points_required}
                      className="bg-[#e52521] hover:bg-[#c91d1a] disabled:opacity-40 text-white font-bold px-2.5 py-1.5 rounded-lg border-2 border-black text-[10px] mario-font shadow-[2px_2px_0px_#000] active:translate-x-0.5 active:translate-y-0.5 transition cursor-pointer whitespace-nowrap"
                    >
                      {redeemingId === coupon.id ? "..." : "BUY"}
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
